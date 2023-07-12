from __future__ import annotations

from .fixtures.mock_extension import MockExtension


def test_constructor() -> None:
    name = "name"
    extension = MockExtension(name)
    assert extension.name == name


def test_to_dict() -> None:
    extension = MockExtension("name")
    assert extension.to_dict() == {}
