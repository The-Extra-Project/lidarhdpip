import json
from pathlib import Path

from pytest import fixture

from py3dtiles.tileset.extension.batch_table_hierarchy_extension import (
    BatchTableHierarchy,
)

DATA_DIRECTORY = Path(__file__).parent / "fixtures"


@fixture()
def batch_table_hierarchy_with_indexes() -> BatchTableHierarchy:
    """
    Programmatically define the reference sample encountered in the
    BTH specification cf
    https://github.com/AnalyticalGraphicsInc/3d-tiles/tree/master/extensions/3DTILES_batch_table_hierarchy#batch-table-json-schema-updates
    :return: the sample as BatchTableHierarchy object.
    """
    bth = BatchTableHierarchy()

    wall_class = bth.add_class("Wall", ["color"])
    wall_class.add_instance({"color": "white"}, [6])
    wall_class.add_instance({"color": "red"}, [6, 10, 11])
    wall_class.add_instance({"color": "yellow"}, [7, 11])
    wall_class.add_instance({"color": "gray"}, [7])
    wall_class.add_instance({"color": "brown"}, [8])
    wall_class.add_instance({"color": "black"}, [8])

    building_class = bth.add_class("Building", ["name", "address"])
    building_class.add_instance({"name": "unit29", "address": "100 Main St"}, [10])
    building_class.add_instance({"name": "unit20", "address": "102 Main St"}, [10])
    building_class.add_instance({"name": "unit93", "address": "104 Main St"}, [9])

    owner_class = bth.add_class("Owner", ["type", "id"])
    owner_class.add_instance({"type": "city", "id": 1120})
    owner_class.add_instance({"type": "resident", "id": 1250})
    owner_class.add_instance({"type": "commercial", "id": 6445})
    return bth


@fixture()
def batch_table_hierarchy_with_instances() -> BatchTableHierarchy:
    bth = BatchTableHierarchy()

    wall_class = bth.add_class("Wall", ["color"])
    building_class = bth.add_class("Building", ["name", "address"])
    owner_class = bth.add_class("Owner", ["type", "id"])

    owner_city = owner_class.add_instance({"type": "city", "id": 1120})
    owner_resident = owner_class.add_instance({"type": "resident", "id": 1250})
    owner_commercial = owner_class.add_instance({"type": "commercial", "id": 6445})

    building_29 = building_class.add_instance(
        {"name": "unit29", "address": "100 Main St"}, [owner_resident]
    )
    building_20 = building_class.add_instance(
        {"name": "unit20", "address": "102 Main St"}, [owner_resident]
    )
    building_93 = building_class.add_instance(
        {"name": "unit93", "address": "104 Main St"}, [owner_city]
    )

    wall_class.add_instance({"color": "white"}, [building_29])
    wall_class.add_instance(
        {"color": "red"}, [building_29, owner_resident, owner_commercial]
    )
    wall_class.add_instance({"color": "yellow"}, [building_20, owner_commercial])
    wall_class.add_instance({"color": "gray"}, [building_20])
    wall_class.add_instance({"color": "brown"}, [building_93])
    wall_class.add_instance({"color": "black"}, [building_93])
    return bth


def test_bth_build_sample_with_indexes_and_compare_reference_file(
    batch_table_hierarchy_with_indexes: BatchTableHierarchy,
) -> None:
    """
    Build the sample, load the version from the reference file and
    compare them (in memory as opposed to "diffing" files)
    """
    json_bth = batch_table_hierarchy_with_indexes.to_dict()

    with (
        DATA_DIRECTORY / "batch_table_hierarchy_reference_sample.json"
    ).open() as reference_file:
        json_reference = json.loads(reference_file.read())

    json_reference.pop("_comment", None)  # Drop the "comment".

    assert json_bth == json_reference


def test_bth_build_sample_with_instances_and_compare_reference_file(
    batch_table_hierarchy_with_instances: BatchTableHierarchy,
) -> None:
    """
    Build the sample, load the version from the reference file and
    compare them (in memory as opposed to "diffing" files)
    """
    json_bth = batch_table_hierarchy_with_instances.to_dict()

    with (
        DATA_DIRECTORY / "batch_table_hierarchy_reference_sample.json"
    ).open() as reference_file:
        json_reference = json.loads(reference_file.read())

    json_reference.pop("_comment", None)  # Drop the "comment".

    assert json_bth == json_reference
