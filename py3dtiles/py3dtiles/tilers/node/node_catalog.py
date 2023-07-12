from __future__ import annotations

import math
import pickle
from typing import TYPE_CHECKING

import lz4.frame as gzip

from py3dtiles.tilers.node.node import Node
from py3dtiles.utils import split_aabb

if TYPE_CHECKING:
    from py3dtiles.utils import OctreeMetadata


class NodeCatalog:
    """NodeCatalog is a store of Node objects.py3dtiles

    Using a NodeCatalog allows to only store a children names
    in nodes, instead of storing a full recursive structure.
    """

    def __init__(
        self, nodes: bytes, name: bytes, octree_metadata: OctreeMetadata
    ) -> None:
        self.nodes: dict[bytes, Node] = {}
        self.root_aabb = octree_metadata.aabb
        self.root_spacing = octree_metadata.spacing
        self.node_bytes: dict[bytes, bytes] = {}
        self._load_from_store(name, nodes)

    def get_node(self, name: bytes) -> Node:
        """Returns the node mathing the given name"""
        if name not in self.nodes:
            spacing = self.root_spacing / math.pow(2, len(name))
            aabb = self.root_aabb
            for i in name:
                aabb = split_aabb(aabb, int(i))
            node = Node(name, aabb, spacing)
            self.nodes[name] = node
        else:
            node = self.nodes[name]
        return node

    def dump(self, name: bytes, max_depth: int) -> bytes:
        """Serialize the stored nodes to a bytes list"""
        node = self.nodes[name]
        if node.dirty:
            self.node_bytes[name] = node.save_to_bytes()

        if node.children is not None and max_depth > 0:
            for n in node.children:
                self.dump(n, max_depth - 1)

        return pickle.dumps(self.node_bytes)

    def _load_from_store(self, name: bytes, data: bytes) -> Node:
        if len(data) > 0:
            out = pickle.loads(gzip.decompress(data))
            for n in out:
                spacing = self.root_spacing / math.pow(2, len(n))
                aabb = self.root_aabb
                for i in n:
                    aabb = split_aabb(aabb, int(i))
                node = Node(n, aabb, spacing)
                node.load_from_bytes(out[n])
                self.node_bytes[n] = out[n]
                self.nodes[n] = node
        else:
            spacing = self.root_spacing / math.pow(2, len(name))
            aabb = self.root_aabb
            for i in name:
                aabb = split_aabb(aabb, int(i))
            node = Node(name, aabb, spacing)
            self.nodes[name] = node

        return self.nodes[name]
