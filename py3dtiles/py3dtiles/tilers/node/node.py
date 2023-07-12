from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
import json
from pathlib import Path
import pickle
from typing import Any, Generator, Iterator, TYPE_CHECKING, TypedDict

import numpy as np
import numpy.typing as npt

from py3dtiles.exceptions import TilerException
from py3dtiles.tilers.pnts import MIN_POINT_SIZE
from py3dtiles.tilers.pnts.pnts_writer import points_to_pnts_file
from py3dtiles.tileset.content import read_binary_tile_content
from py3dtiles.tileset.content.feature_table import SemanticPoint
from py3dtiles.typing import BoundingVolumeBoxDictType, ContentType, TileDictType
from py3dtiles.utils import (
    aabb_size_to_subdivision_type,
    node_from_name,
    node_name_to_path,
    SubdivisionType,
)
from .distance import xyz_to_child_index
from .points_grid import Grid

if TYPE_CHECKING:
    from .node_catalog import NodeCatalog
    from typing_extensions import NotRequired


def node_to_tileset(
    args: tuple[Node, Path, npt.NDArray[np.float32], Node | None, int]
) -> TileDictType | None:
    return args[0].to_tileset(args[1], args[2], args[3], args[4], None)


class _DummyNodeDictType(TypedDict):
    children: NotRequired[list[bytes]]
    grid: NotRequired[Grid]
    points: NotRequired[
        list[
            tuple[npt.NDArray[np.float32], npt.NDArray[np.uint8], npt.NDArray[np.uint8]]
        ]
    ]


class DummyNode:
    def __init__(self, _bytes: _DummyNodeDictType) -> None:
        if "children" in _bytes:
            self.children: list[bytes] | None = _bytes["children"]
            self.grid = _bytes["grid"]
        else:
            self.children = None
            self.points = _bytes["points"]


class Node:
    """docstring for Node"""

    __slots__ = (
        "name",
        "aabb",
        "aabb_size",
        "inv_aabb_size",
        "aabb_center",
        "spacing",
        "pending_xyz",
        "pending_rgb",
        "pending_classification",
        "children",
        "grid",
        "points",
        "dirty",
    )

    def __init__(
        self, name: bytes, aabb: npt.NDArray[np.float64 | np.float32], spacing: float
    ) -> None:
        super().__init__()
        self.name = name
        self.aabb = aabb.astype(
            np.float32
        )  # TODO remove astype once the whole typing is done (and once data type issues on numpy arrays are fixed).
        self.aabb_size = np.maximum(self.aabb[1] - self.aabb[0], MIN_POINT_SIZE)
        self.inv_aabb_size = 1.0 / self.aabb_size
        self.aabb_center = (self.aabb[0] + self.aabb[1]) * 0.5
        self.spacing = spacing
        self.pending_xyz: list[npt.NDArray[np.float32]] = []
        self.pending_rgb: list[npt.NDArray[np.uint8]] = []
        self.pending_classification: list[npt.NDArray[np.uint8]] = []
        self.children: list[bytes] | None = None
        self.grid = Grid(self)
        self.points: list[
            tuple[npt.NDArray[np.float32], npt.NDArray[np.uint8], npt.NDArray[np.uint8]]
        ] = []
        self.dirty = False

    def save_to_bytes(self) -> bytes:
        sub_pickle: dict[str, Any] = {}
        if self.children is not None:
            sub_pickle["children"] = self.children
            sub_pickle["grid"] = self.grid
        else:
            sub_pickle["points"] = self.points

        return pickle.dumps(sub_pickle)

    def load_from_bytes(self, byt: bytes) -> None:
        sub_pickle = pickle.loads(byt)
        if "children" in sub_pickle:
            self.children = sub_pickle["children"]
            self.grid = sub_pickle["grid"]
        else:
            self.points = sub_pickle["points"]

    def insert(
        self,
        scale: float,
        xyz: npt.NDArray[np.float32],
        rgb: npt.NDArray[np.uint8],
        classification: npt.NDArray[np.uint8],
        make_empty_node: bool = False,
    ) -> None:
        if make_empty_node:
            self.children = []
            self.pending_xyz += [xyz]
            self.pending_rgb += [rgb]
            self.pending_classification += [classification]
            return

        # fastpath
        if self.children is None:
            self.points.append((xyz, rgb, classification))
            count = sum([xyz.shape[0] for xyz, rgb, classification in self.points])
            # stop subdividing if spacing is 1mm
            if count >= 20000 and self.spacing > 0.001 * scale:
                self._split(scale)
            self.dirty = True

            return

        # grid based insertion
        (
            remainder_xyz,
            remainder_rgb,
            remainder_classification,
            needs_balance,
        ) = self.grid.insert(self.aabb[0], self.inv_aabb_size, xyz, rgb, classification)

        if needs_balance:
            self.grid.balance(self.aabb_size, self.aabb[0], self.inv_aabb_size)
            self.dirty = True

        self.dirty = self.dirty or (len(remainder_xyz) != len(xyz))

        if len(remainder_xyz) > 0:
            self.pending_xyz += [remainder_xyz]
            self.pending_rgb += [remainder_rgb]
            self.pending_classification += [remainder_classification]

    def needs_balance(self) -> bool:
        if self.children is not None:
            return self.grid.needs_balance()
        return False

    def flush_pending_points(self, catalog: NodeCatalog, scale: float) -> None:
        for name, xyz, rgb, classification in self._get_pending_points():
            catalog.get_node(name).insert(scale, xyz, rgb, classification)
        self.pending_xyz = []
        self.pending_rgb = []
        self.pending_classification = []

    def dump_pending_points(self) -> list[tuple[bytes, bytes, int]]:
        result = [
            (
                name,
                pickle.dumps(
                    {"xyz": xyz, "rgb": rgb, "classification": classification}
                ),
                len(xyz),
            )
            for name, xyz, rgb, classification in self._get_pending_points()
        ]

        self.pending_xyz = []
        self.pending_rgb = []
        self.pending_classification = []
        return result

    def get_pending_points_count(self) -> int:
        return sum([xyz.shape[0] for xyz in self.pending_xyz])

    def _get_pending_points(
        self,
    ) -> Iterator[
        tuple[
            bytes, npt.NDArray[np.float32], npt.NDArray[np.uint8], npt.NDArray[np.uint8]
        ]
    ]:
        if not self.pending_xyz:
            return

        pending_xyz_arr = np.concatenate(self.pending_xyz)
        pending_rgb_arr = np.concatenate(self.pending_rgb)
        pending_classification_arr = np.concatenate(self.pending_classification)
        t = aabb_size_to_subdivision_type(self.aabb_size)
        if t == SubdivisionType.QUADTREE:
            indices = xyz_to_child_index(
                pending_xyz_arr,
                np.array(
                    [self.aabb_center[0], self.aabb_center[1], self.aabb[1][2]],
                    dtype=np.float32,
                ),
            )
        else:
            indices = xyz_to_child_index(pending_xyz_arr, self.aabb_center)

        # unique children list
        childs = np.unique(indices)

        # make sure all children nodes exist
        for child in childs:
            name = "{}{}".format(self.name.decode("ascii"), child).encode("ascii")
            # create missing nodes, only for remembering they exist.
            # We don't want to serialize them
            # probably not needed...
            if self.children is not None and name not in self.children:
                self.children += [name]
                self.dirty = True
                # print('Added node {}'.format(name))

            mask = np.where(indices - child == 0)
            xyz = pending_xyz_arr[mask]
            if len(xyz) > 0:
                yield name, xyz, pending_rgb_arr[mask], pending_classification_arr[mask]

    def _split(self, scale: float) -> None:
        self.children = []
        for xyz, rgb, classification in self.points:
            self.insert(scale, xyz, rgb, classification)
        self.points = []

    def get_point_count(
        self, node_catalog: NodeCatalog, max_depth: int, depth: int = 0
    ) -> int:
        if self.children is None:
            return sum([xyz.shape[0] for xyz, rgb, classification in self.points])
        else:
            count = self.grid.get_point_count()
            if depth < max_depth:
                for n in self.children:
                    count += node_catalog.get_node(n).get_point_count(
                        node_catalog, max_depth, depth + 1
                    )
            return count

    @staticmethod
    def get_points(
        data: Node | DummyNode, include_rgb: bool, include_classification: bool
    ) -> npt.NDArray[np.uint8]:  # todo remove staticmethod
        if data.children is None:
            points = data.points
            xyz = (
                np.concatenate(tuple([xyz for xyz, rgb, classification in points]))
                .view(np.uint8)
                .ravel()
            )

            if include_rgb:
                rgb = np.concatenate(
                    tuple([rgb for xyz, rgb, classification in points])
                ).ravel()
            else:
                rgb = np.array([], dtype=np.uint8)

            if include_classification:
                classification = np.concatenate(
                    tuple([classification for xyz, rgb, classification in points])
                ).ravel()
            else:
                classification = np.array([], dtype=np.uint8)

            return np.concatenate((xyz, rgb, classification))
        else:
            return data.grid.get_points(include_rgb, include_classification)

    def get_child_names(self) -> Generator[bytes, None, None]:
        for number_child in range(8):
            yield f"{self.name.decode('ascii')}{number_child}".encode("ascii")

    def to_tileset(
        self,
        folder: Path,
        scale: npt.NDArray[np.float32],
        parent_node: Node | None = None,
        depth: int = 0,
        pool_executor: ProcessPoolExecutor | None = None,
    ) -> TileDictType | None:
        # create child tileset parts
        # if their size is below of 100 points, they will be merged in this node.
        children_tileset_parts: list[TileDictType] = []
        parameter_to_compute: list[
            tuple[Node, Path, npt.NDArray[np.float32], Node, int]
        ] = []
        for child_name in self.get_child_names():
            child_node = node_from_name(child_name, self.aabb, self.spacing)
            child_pnts_path = node_name_to_path(folder, child_name, ".pnts")

            if child_pnts_path.exists():
                # multi thread is only allowed on nodes where there are no prune
                # a simple rule is: only is there is not a parent node
                if pool_executor and parent_node is None:
                    parameter_to_compute.append(
                        (child_node, folder, scale, self, depth + 1)
                    )
                else:
                    children_tileset_part = child_node.to_tileset(
                        folder, scale, self, depth + 1
                    )
                    if (
                        children_tileset_part is not None
                    ):  # return None if the child has been merged
                        children_tileset_parts.append(children_tileset_part)

        if pool_executor and parent_node is None:
            children_tileset_parts = [
                t
                for t in pool_executor.map(node_to_tileset, parameter_to_compute)
                if t is not None
            ]

        pnts_path = node_name_to_path(folder, self.name, ".pnts")
        tile = read_binary_tile_content(pnts_path)
        fth = tile.body.feature_table.header
        xyz = tile.body.feature_table.body.position

        # check if this node should be merged in the parent.
        prune = False  # prune only if the node is a leaf

        # If this child is small enough, merge in the current tile
        if parent_node is not None and depth > 1 and fth.points_length < 100:
            parent_pnts_path = node_name_to_path(folder, parent_node.name, ".pnts")
            parent_tile = read_binary_tile_content(parent_pnts_path)
            parent_fth = parent_tile.body.feature_table.header

            parent_xyz = parent_tile.body.feature_table.body.position

            if (
                parent_fth.colors != SemanticPoint.NONE
                and parent_tile.body.feature_table.body.color is not None
            ):
                parent_rgb = parent_tile.body.feature_table.body.color
            else:
                parent_rgb = np.array([], dtype=np.uint8)

            if "Classification" in parent_tile.body.batch_table.header.data:
                parent_classification = (
                    parent_tile.body.batch_table.get_binary_property("Classification")
                )
            else:
                parent_classification = np.array([], dtype=np.uint8)

            parent_xyz_float = parent_xyz.reshape((parent_fth.points_length, 3))
            # update aabb based on real values
            parent_aabb = np.array(
                [
                    np.amin(parent_xyz_float, axis=0),
                    np.amax(parent_xyz_float, axis=0),
                ]
            )

            parent_xyz = np.concatenate((parent_xyz, xyz))

            if fth.colors != SemanticPoint.NONE:
                if tile.body.feature_table.body.color is None:
                    raise TilerException(
                        "If the parent has color data, the children must also have color data."
                    )
                parent_rgb = np.concatenate(
                    (parent_rgb, tile.body.feature_table.body.color)
                )

            if "Classification" in tile.body.batch_table.header.data:
                parent_classification = np.concatenate(
                    (
                        parent_classification,
                        tile.body.batch_table.get_binary_property("Classification"),
                    )
                )

            # update aabb
            xyz_float = xyz.view(np.float32).reshape((fth.points_length, 3))

            parent_aabb[0] = np.amin(
                [parent_aabb[0], np.min(xyz_float, axis=0)], axis=0
            )
            parent_aabb[1] = np.amax(
                [parent_aabb[1], np.max(xyz_float, axis=0)], axis=0
            )

            parent_pnts_path.unlink()
            points_to_pnts_file(
                parent_node.name,
                np.concatenate(
                    (parent_xyz.view(np.uint8), parent_rgb, parent_classification)
                ),
                folder,
                len(parent_rgb) != 0,
                len(parent_classification) != 0,
            )
            pnts_path.unlink()
            prune = True

        content: ContentType | None = None
        if not prune:
            content = {"uri": str(pnts_path.relative_to(folder))}
            xyz_float = xyz.view(np.float32).reshape((fth.points_length, 3))

            # update aabb based on real values
            aabb = np.array([np.amin(xyz_float, axis=0), np.amax(xyz_float, axis=0)])

            center = ((aabb[0] + aabb[1]) * 0.5).tolist()
            half_size = ((aabb[1] - aabb[0]) * 0.5).tolist()
            bounding_volume: BoundingVolumeBoxDictType = {
                "box": [
                    center[0],
                    center[1],
                    center[2],
                    half_size[0],
                    0,
                    0,
                    0,
                    half_size[1],
                    0,
                    0,
                    0,
                    half_size[2],
                ]
            }
        else:
            # if it is a leaf that should be pruned
            if not children_tileset_parts:
                return None

            # recompute the aabb in function of children
            aabb = None
            for child_tileset_part in children_tileset_parts:
                bounding_box = child_tileset_part["boundingVolume"].get("box")
                if not isinstance(bounding_box, list):
                    raise ValueError("bounding_box must be a list")
                if bounding_box is None:
                    raise NotImplementedError(
                        "bounding_box can only be a bounding volume box"
                    )

                center = np.array(bounding_box[:3])
                half_size = np.array(bounding_box[3::4])

                child_aabb = np.array([center + half_size, center - half_size])

                if aabb is None:
                    aabb = child_aabb
                else:
                    aabb[0] = np.amin([aabb[0], child_aabb[0]], axis=0)
                    aabb[1] = np.amax([aabb[1], child_aabb[1]], axis=0)

            if aabb is None:
                raise TilerException("aabb shouldn't be None")

            center = ((aabb[0] + aabb[1]) * 0.5).tolist()
            half_size = ((aabb[1] - aabb[0]) * 0.5).tolist()
            bounding_volume = {
                "box": [
                    center[0],
                    center[1],
                    center[2],
                    half_size[0],
                    0,
                    0,
                    0,
                    half_size[1],
                    0,
                    0,
                    0,
                    half_size[2],
                ]
            }

        tileset: TileDictType = {
            "boundingVolume": bounding_volume,
            "geometricError": 10 * self.spacing / scale[0],
        }
        if content is not None:
            tileset["content"] = content

        if children_tileset_parts:
            tileset["children"] = children_tileset_parts
        else:
            tileset["geometricError"] = 0.0

        if (
            len(self.name) > 0
            and children_tileset_parts
            and len(json.dumps(tileset)) > 100000
        ):
            tileset = split_tileset(tileset, self.name.decode(), folder)

        return tileset


def split_tileset(
    tile_dict: TileDictType, split_name: str, folder: Path
) -> TileDictType:
    tileset = {
        "asset": {
            "version": "1.0",
        },
        "refine": "ADD",
        "geometricError": tile_dict["geometricError"],
        "root": tile_dict,
    }
    tileset_name = f"tileset.{split_name}.json"
    with (folder / tileset_name).open("w") as f:
        f.write(json.dumps(tileset))
    tile_dict["content"] = {"uri": tileset_name}
    del tile_dict["children"]

    return tile_dict
