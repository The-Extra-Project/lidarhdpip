from __future__ import annotations

from py3dtiles.tileset.extension import BaseExtension
from py3dtiles.typing import ExtensionDictType


class MockExtension(BaseExtension):
    @classmethod
    def from_dict(cls, extension_dict: ExtensionDictType) -> MockExtension:
        return cls("MockExtension")

    def to_dict(self) -> ExtensionDictType:
        return {}
