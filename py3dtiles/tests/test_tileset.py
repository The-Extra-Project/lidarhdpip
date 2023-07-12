from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
from typing import Generator

from pytest import fixture

from py3dtiles.convert import convert
from py3dtiles.tileset import BoundingVolumeBox, Tile, TileSet
from .fixtures.mock_extension import MockExtension

DATA_DIRECTORY = Path(__file__).parent / "fixtures"


@fixture
def tileset() -> TileSet:
    """
    Programmatically define a tileset sample encountered in the
    TileSet json header specification cf
    https://github.com/AnalyticalGraphicsInc/3d-tiles/tree/master/specification#tileset-json
    :return: a TileSet object.
    """
    tile_set = TileSet()
    bounding_volume = BoundingVolumeBox()
    bounding_volume.set_from_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    root_tile = Tile(geometric_error=3.14159, bounding_volume=bounding_volume)
    # Setting the mode to the default mode does not really change things.
    # The following line is thus just here ot test the "callability" of
    # set_refine_mode():
    root_tile.set_refine_mode("ADD")
    tile_set.root_tile = root_tile

    extension = MockExtension("Test")
    tile_set.extensions[extension.name] = extension
    tile_set.extensions_used.add(extension.name)

    return tile_set


@fixture
def tileset_on_disk_with_sub_tileset_path() -> Generator[Path, None, None]:
    tmp_dir = Path("tmp/")
    tmp_dir.mkdir(exist_ok=True)
    convert(DATA_DIRECTORY / "simple.xyz", outfolder=tmp_dir, overwrite=True)

    sub_tileset_path = tmp_dir / "tileset.json"
    main_tileset_path = tmp_dir / "upper_tileset.json"
    sub_tileset = TileSet.from_file(sub_tileset_path)

    tileset = TileSet()
    tileset.root_tile.content_uri = Path("tileset.json")
    tileset.root_tile.bounding_volume = copy.deepcopy(
        sub_tileset.root_tile.bounding_volume
    )
    tileset.root_tile.transform = copy.deepcopy(sub_tileset.root_tile.transform)
    tileset.write_as_json(main_tileset_path)

    yield main_tileset_path

    shutil.rmtree(tmp_dir, ignore_errors=True)


def test_constructor() -> None:
    tile_set = TileSet()
    assert tile_set.asset.to_dict() == {"version": "1.0"}
    assert tile_set.extensions == {}
    assert tile_set.geometric_error == 500
    assert isinstance(tile_set.root_tile, Tile)


def test_to_dict(tileset: TileSet) -> None:
    assert tileset.to_dict() == {
        "root": {
            "boundingVolume": {
                "box": [
                    1.0,
                    2.0,
                    3.0,
                    4.0,
                    5.0,
                    6.0,
                    7.0,
                    8.0,
                    9.0,
                    10.0,
                    11.0,
                    12.0,
                ]
            },
            "geometricError": 3.14159,
            "refine": "ADD",
        },
        "extensions": {"Test": {}},
        "extensionsUsed": ["Test"],
        "geometricError": 500,
        "asset": {"version": "1.0"},
    }


def test_from_dict() -> None:
    tmp_dir = Path("tmp/")
    tmp_dir.mkdir(exist_ok=True)

    convert(DATA_DIRECTORY / "simple.xyz", outfolder=tmp_dir, overwrite=True)

    assert Path(tmp_dir, "tileset.json").exists()
    assert Path(tmp_dir, "r.pnts").exists()

    with (tmp_dir / "tileset.json").open() as f:
        tileset_dict = json.load(f)

    tileset = TileSet.from_dict(tileset_dict)
    tileset.root_uri = tmp_dir

    assert tileset.to_dict() == tileset_dict

    shutil.rmtree(tmp_dir, ignore_errors=True)


def test_delete_on_disk(tileset_on_disk_with_sub_tileset_path: Path) -> None:
    # This test only checks if delete_on_disk doesn't delete sub-tileset

    tmp_folder = tileset_on_disk_with_sub_tileset_path.parent
    assert (tmp_folder / "tileset.json").exists()
    assert (tmp_folder / "upper_tileset.json").exists()

    tileset = TileSet.from_file(tileset_on_disk_with_sub_tileset_path)
    tileset.delete_on_disk(tmp_folder / "upper_tileset.json")

    assert (tmp_folder / "tileset.json").exists()
    assert (tmp_folder / "r.pnts").exists()
    assert not (tmp_folder / "upper_tileset.json").exists()


def test_delete_on_disk_with_sub_tileset(
    tileset_on_disk_with_sub_tileset_path: Path,
) -> None:
    # This test manly checks if delete_on_disk removes correctly all tile contents (binary and sub tileset)

    tmp_folder = tileset_on_disk_with_sub_tileset_path.parent
    assert (tmp_folder / "tileset.json").exists()
    assert (tmp_folder / "upper_tileset.json").exists()

    tileset = TileSet.from_file(tileset_on_disk_with_sub_tileset_path)
    tileset.delete_on_disk(tmp_folder / "upper_tileset.json", delete_sub_tileset=True)

    assert not (tmp_folder / "tileset.json").exists()
    assert not (tmp_folder / "r.pnts").exists()
    assert not (tmp_folder / "upper_tileset.json").exists()
