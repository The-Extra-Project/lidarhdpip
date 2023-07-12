.. _api:

.. |check| raw:: html

    <input checked=""  type="checkbox" onclick="return false;">

.. |uncheck| raw:: html

    <input type="checkbox" onclick="return false;">

API usage
=========

Tileset manipulation
--------------------
The tileset module contains all the classes to represent a dataset in 3D Tiles format,
whether it is the `tileset.json` file or the content of the tiles (sub-tileset, pnts or b3dm, there is no i3dm support).

.. note::

    Currently, Py3dtiles partially supports the 3d Tiles standard at version 1.0. There is work to support the 1.1 standard. The main feature of 1.1 is the dropping of specific formats (pnts, b3dm and i3dm) in favor of the gltf format.

There is work to support the 1.1 standard. The main feature of 1.1 is the dropping of specific formats (pnts, b3dm and i3dm)
in favor of the gltf format.

Structure of a tileset in Py3dtiles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At the top of the hierarchy, there is the class `TileSet` which will contain a root tile which is an instance of a `Tile`.
Then this root tile can contain content (`TileContent` or again a `TileSet`) and child tiles,
which themselves can contain content and children.

TileSet class
~~~~~~~~~~~~~

This class will contain the properties defined by the standard as well as methods related to reading and writing
an entire tileset. Here is the current state of the properties supported by Py3dtiles:

- |check| `asset`
    - |check| `version`
    - |check| `tilesetVersion`
    - |check| `extensions`
    - |check| `extras` (partially)
- |uncheck| `properties`
- |uncheck| `schema` (version 1.1)
- |uncheck| `schemaUri` (version 1.1)
- |uncheck| `statistics` (version 1.1)
- |uncheck| `groups` (version 1.1)
- |uncheck| `metadata` (version 1.1)
- |check| `geometricError`
- |check| `root` (the name in Py3dtiles is `root_tile`)
- |check| `extensionsUsed`
- |check| `extensionsRequired`
- |check| `extensions`
- |check| `extras`

**Create a tileset from scratch:**

.. code-block:: python

    >>> from py3dtiles.tileset import TileSet
    >>>
    >>> tileset = TileSet()
    >>>
    >>> # when creating a tileset from scratch, the first tile (named root_tile) is initialized
    >>> tileset.root_tile
    <py3dtiles.tileset.tile.Tile object at 0x...>

**Read and write a tileset:**

.. code-block:: python

    >>> # it is possible to load a tileset from the json content
    >>> import json
    >>> from pathlib import Path
    >>>
    >>> from py3dtiles.tileset import TileSet
    >>>
    >>> tileset_path = Path("tests/fixtures/tiles/tileset.json")
    >>> with tileset_path.open() as f:
    ...     tileset = TileSet.from_dict(json.load(f))
    >>> tileset.root_uri = tileset_path.parent
    >>> tileset
    <py3dtiles.tileset.tileset.TileSet object at 0x...>
    >>>
    >>> # or more simply
    >>> tileset = TileSet.from_file(tileset_path)
    >>>
    >>> # a tileset can be written to the disk
    >>> # if you want the content of the tiles to be written too, use write_to_directory
    >>> new_tileset_path = Path("my3dtiles/tileset.json")
    >>> new_tileset_path.parent.mkdir()
    >>> tileset.write_as_json(new_tileset_path)

When reading a tileset, the tile content loading is done lazily, i.e. one loads only the `tileset.json` file and the tile contents is loaded only when needed.

Tile class
~~~~~~~~~~

The Tile class represents a tile in the `tileset.json`. It will contain the properties defined by the standard:

- |check| boundingVolume (only the bounding volume box)
- |uncheck| viewerRequestVolume
- |check| geometricError
- |check| refine
- |check| transform
- |check| content
    - |check| uri
    - |check| boundingVolume (partially)
- |uncheck| contents (version 1.1)
- |uncheck| metadata (version 1.1)
- |uncheck| implicitTiling (version 1.1)
- |check| children
- |check| `extensions`
- |check| `extras`

.. warning::
    In py3dtiles the content data and the content uri are in 2 separate variables.

.. code-block:: python

    >>> from pathlib import Path
    >>>
    >>> from py3dtiles.tileset import Tile
    >>> from py3dtiles.tileset.content import read_binary_tile_content
    >>>
    >>> tile = Tile()
    >>> # the pnts is loaded and linked to the tile
    >>> tile.tile_content = read_binary_tile_content(Path("tests/fixtures/pointCloudRGB.pnts"))
    >>> # the uri that will be written in the tileset.json (and the path where the pnts will be writen)
    >>> tile.content_uri = Path("tiles/1.pnts")


Bounding volume
~~~~~~~~~~~~~~~
There are 3 types of bounding volume:

- |check| Bounding volume box
- |uncheck| Bounding volume region
- |uncheck| Bounding volume sphere

**Creation of a bounding volume box**

.. code-block:: python

    >>> import numpy as np
    >>>
    >>> from py3dtiles.tileset import BoundingVolumeBox
    >>>
    >>> center = [0, 0, 0]
    >>> x_half_axis = [3, 3, 3]
    >>> y_half_axis = [3, 3, 3]
    >>> z_half_axis = [1, 0, 0]
    >>>
    >>> bounding_box = BoundingVolumeBox()
    >>> bounding_box.set_from_list([*center, *x_half_axis, *y_half_axis, *z_half_axis])
    >>> bounding_box.to_dict()
    {'box': [0.0, 0.0, 0.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 1.0, 0.0, 0.0]}
    >>>
    >>> points = np.array((
    ... (1, 0, 0),
    ... (3, 2, 1),
    ... (4, 6, 8),
    ... (-1, -5, -9),
    ... ))
    >>> bounding_box.set_from_points(points)
    >>> bounding_box.to_dict()
    {'box': [1.5, 0.5, -0.5, 2.5, 0.0, 0.0, 0.0, 5.5, 0.0, 0.0, 0.0, 8.5]}

Extension management
~~~~~~~~~~~~~~~~~~~~

When you add an extension somewhere in a tileset, you must add the name of the extension in the attribute `extensionUsed`
of the class `TileSet` like this:

.. code-block:: python

    >>> from py3dtiles.tileset import TileSet
    >>> from py3dtiles.tileset.extension import BatchTableHierarchy
    >>>
    >>> tileset = TileSet()
    >>>
    >>> extension = BatchTableHierarchy()
    >>>
    >>> tileset.extensions_used.add(extension.name)
    >>> # Furthermore, if the extension is necessary to display the tileset, you should add the name in extensionsRequired
    >>> tileset.extensions_required.add(extension.name)

Since these 2 attributes are sets, the name of an extension can be added several times.

.. note::
   This section should be improved.

Specific exceptions
~~~~~~~~~~~~~~~~~~~

If during reading, manipulation or writing, there is a problem related to the standard,
an exception of type `Py3dtilesException` (or inherited from it) will be raised.

.. code-block:: python

    >>> from py3dtiles.tileset import Tile
    >>>
    >>> tile = Tile()
    >>> tile.to_dict()
    Traceback (most recent call last):
    py3dtiles.exceptions.InvalidTilesetError: Bounding volume is not set

Tileset creation example
~~~~~~~~~~~~~~~~~~~~~~~~

This basic example aims to show a set of methods to create, manipulate and write a tileset.

.. code-block:: python

    >>> from pathlib import Path
    >>>
    >>> import laspy
    >>> import numpy as np
    >>>
    >>> from py3dtiles.tileset import Tile, TileSet
    >>> from py3dtiles.tileset.content import Pnts
    >>> from py3dtiles.tileset.content.feature_table import FeatureTableHeader, SemanticPoint
    >>>
    >>> with laspy.open("tests/fixtures/with_srs_3950.las") as f:
    ...     las_data = f.read()
    >>> points = las_data.points
    >>>
    >>> # Get few points for the root tile
    >>> indexes = np.random.choice(len(points), 100)
    >>> point_part = points[indexes]
    >>> positions = np.vstack((point_part.x, point_part.y, point_part.z)).T
    >>> feature_table_header = FeatureTableHeader.from_semantic(
    ...     SemanticPoint.POSITION, None, None, nb_points = 100
    ... )
    >>> root_tile = Tile(refine_mode="REPLACE", content_uri=Path("root.pnts"))
    >>> root_tile.tile_content = Pnts.from_features(feature_table_header, positions.flatten())
    >>> root_tile.bounding_volume = BoundingVolumeBox()
    >>> root_tile.bounding_volume.set_from_points(positions)
    >>>
    >>> # Split the points in 4 parts
    >>> split_len = len(points) // 4
    >>> splits = [
    ...     (0, split_len),
    ...     (split_len, split_len*2),
    ...     (split_len*2, split_len*3),
    ...     (split_len*3, None),
    ... ]
    >>> for start, end in splits:
    ...     point_part = points[start : end]
    ...     positions = np.vstack((point_part.x, point_part.y, point_part.z)).T
    ...     feature_table_header = FeatureTableHeader.from_semantic(
    ...         SemanticPoint.POSITION, None, None, nb_points = len(point_part)
    ...     )
    ...     tile = Tile(content_uri=Path(f"{start}.pnts"))
    ...     tile.tile_content = Pnts.from_features(feature_table_header, positions.flatten())
    ...     tile.bounding_volume = BoundingVolumeBox()
    ...     tile.bounding_volume.set_from_points(positions)
    ...     root_tile.add_child(tile)
    >>>
    >>> # Create the tileset
    >>> tileset = TileSet()
    >>> tileset.root_tile = root_tile
    >>> tileset_path = Path("my3dtiles2/tileset.json")
    >>> tileset_path.parent.mkdir()
    >>> tileset.write_to_directory(tileset_path)

Tile content
------------

The py3dtiles module provides some classes to fit into the
specification:

- *TileContent* with a header *TileContentHeader* and a body *TileContentBody*
- *TileContentHeader* represents the metadata of the tile (magic value, version, ...)
- *TileContentBody* contains varying semantic and geometric data depending on the the tile's type

Moreover, a utility module *tile_content_reader.py* provides a function *read_binary_tile_content* to read a tile
file as well as a simple command line tool to retrieve basic information about a tile:
**py3dtiles info**. We also provide a utility to generate a tileset from a list of 3D models in
WKB format or stored in a postGIS table.


Point Cloud
~~~~~~~~~~~

Points Tile Format:
https://docs.ogc.org/cs/22-025r4/22-025r4.html#toc29

In the current implementation, the *Pnts* class only contains a *FeatureTable*
(*FeatureTableHeader* and a *FeatureTableBody*, which contains features of type
*Feature*).

**How to read a .pnts file**

.. code-block:: python

    >>> from pathlib import Path
    >>>
    >>> from py3dtiles.tileset.content import Pnts, read_binary_tile_content
    >>>
    >>> filename = Path('tests/fixtures/pointCloudRGB.pnts')
    >>>
    >>> # read the file
    >>> pnts = read_binary_tile_content(filename)
    >>>
    >>> # pnts is an instance of the Pnts class
    >>> pnts
    <py3dtiles.tileset.content.pnts.Pnts object at 0x...>
    >>>
    >>> # extract information about the pnts header
    >>> pnts_header = pnts.header
    >>> pnts_header
    <py3dtiles.tileset.content.pnts.PntsHeader object at 0x...>
    >>> pnts_header.magic_value
    b'pnts'
    >>> pnts_header.tile_byte_length
    15176
    >>>
    >>> # extract the feature table
    >>> feature_table = pnts.body.feature_table
    >>> feature_table
    <py3dtiles.tileset.content.feature_table.FeatureTable object at 0x...>
    >>>
    >>> # display feature table header
    >>> feature_table.header.to_json()
    {'POINTS_LENGTH': 1000, 'RTC_CENTER': [1215012.8828876738, -4736313.051199594, 4081605.22126042], 'POSITION': {'byteOffset': 0}, 'RGB': {'byteOffset': 12000}}
    >>>
    >>> # extract positions and colors of the first point
    >>> feature_table.get_feature_at(0)
    (array([ 2.19396   ,  4.489685  , -0.17107764], dtype=float32), array([ 44, 243, 209], dtype=uint8), None)
    >>> feature_table.get_feature_position_at(0)
    array([ 2.19396   ,  4.489685  , -0.17107764], dtype=float32)
    >>> feature_table.get_feature_color_at(0)
    array([ 44, 243, 209], dtype=uint8)

**How to write a .pnts file**

To write a Point Cloud file, you have to build a numpy array with the
corresponding data type.

.. code-block:: python

    >>> from pathlib import Path
    >>>
    >>> import numpy as np
    >>>
    >>> from py3dtiles.tileset.content import Pnts
    >>> from py3dtiles.tileset.content.feature_table import FeatureTableHeader, SemanticPoint
    >>>
    >>> # create a position array of 2 points
    >>> positions = np.array([
    ...     (4.489, 2.19, -0.17),
    ...     (8.65, 12.2, -0.17),
    ... ], dtype=np.float32).flatten()
    >>>
    >>> # create the feature table header that defines the structure of pnts
    >>> feature_table_header = FeatureTableHeader.from_semantic(SemanticPoint.POSITION, None, None, nb_points = 2)
    >>>
    >>> # create the pnts
    >>> pnts = Pnts.from_features(feature_table_header, positions)
    >>>
    >>> # the pnts is complete
    >>> pnts.body.feature_table.header.to_json()
    {'POINTS_LENGTH': 2, 'POSITION': {'byteOffset': 0}}
    >>>
    >>> # to save our tile as a .pnts file
    >>> pnts.save_as(Path("mypoints.pnts"))


Batched 3D Model
~~~~~~~~~~~~~~~~

Batched 3D Model Tile Format:
https://docs.ogc.org/cs/22-025r4/22-025r4.html#toc27

**How to read a .b3dm file**

.. code-block:: python

    >>> from pathlib import Path
    >>>
    >>> from py3dtiles.tileset.content import B3dm, read_binary_tile_content
    >>>
    >>> filename = Path('tests/fixtures/dragon_low.b3dm')
    >>>
    >>> # read the file
    >>> b3dm = read_binary_tile_content(filename)
    >>>
    >>> # b3dm is an instance of the B3dm class
    >>> b3dm
    <py3dtiles.tileset.content.b3dm.B3dm object at 0x...>
    >>>
    >>> # extract information about the b3dm header
    >>> b3dm_header = b3dm.header
    >>> b3dm_header
    <py3dtiles.tileset.content.b3dm.B3dmHeader object at 0x...>
    >>> b3dm_header.magic_value
    b'b3dm'
    >>> b3dm_header.tile_byte_length
    47246
    >>>
    >>> # extract the glTF
    >>> gltf = b3dm.body.gltf
    >>> gltf
    <py3dtiles.tileset.content.gltf.GlTF object at 0x...>
    >>>
    >>> # display gltf header's asset field
    >>> gltf.header['asset']
    {'generator': 'OBJ2GLTF', 'premultipliedAlpha': True, 'profile': {'api': 'WebGL', 'version': '1.0'}, 'version': '1.0'}

**How to write a .b3dm file**

To write a Batched 3D Model file, you have to import the geometry from a wkb
file containing polyhedralsurfaces or multipolygons.

.. code-block:: python

    >>> from pathlib import Path
    >>>
    >>> import numpy as np
    >>>
    >>> from py3dtiles.tilers.b3dm.wkb_utils import TriangleSoup
    >>> from py3dtiles.tileset.content import B3dm, GlTF
    >>>
    >>> # load a wkb file
    >>> wkb = open('tests/fixtures/building.wkb', 'rb').read()
    >>>
    >>> # define the geometry's bounding box
    >>> box = [[-8.75, -7.36, -2.05], [8.80, 7.30, 2.05]]
    >>>
    >>> # define the geometry's world transformation
    >>> transform = np.array([
    ...             [1, 0, 0, 1842015.125],
    ...             [0, 1, 0, 5177109.25],
    ...             [0, 0, 1, 247.87364196777344],
    ...             [0, 0, 0, 1]], dtype=float)
    >>> transform = transform.flatten('F')
    >>>
    >>> # use the TriangleSoup helper class to transform the wkb into arrays
    >>> # of points and normals
    >>> ts = TriangleSoup.from_wkb_multipolygon(wkb)
    >>> positions = ts.get_position_array()
    >>> normals = ts.get_normal_array()
    >>> # generate the glTF part from the binary arrays.
    >>> # notice that from_binary_arrays accepts array of geometries
    >>> # for batching purposes.
    >>> geometry = { 'position': positions, 'normal': normals, 'bbox': box }
    >>> gltf = GlTF.from_binary_arrays([geometry], transform)
    >>>
    >>> # create a b3dm directly from the glTF.
    >>> b3dm = B3dm.from_gltf(gltf)
    >>>
    >>> # to save our tile content as a .b3dm file
    >>> b3dm.save_as(Path("mymodel.b3dm"))

Tiler tools
-----------

Here is an example of calling the conversion tool. An input CRS is needed as the `crs_out` parameter is specified. As the `.las` file contains this information, it is not necessary to specify it.

The CRS can be overwritten by specifying a value for the `crs_in` parameter and by setting the `force_crs_in` parameter to `True`.

In the snippet below, the number of jobs is set to 2. The main process will manage 2 processes that will read the laz file, transform and write the 3D Tiles.

.. code-block:: python

    >>> from pathlib import Path
    >>>
    >>> from pyproj import CRS
    >>>
    >>> from py3dtiles.convert import convert
    >>>
    >>> las_path = Path("tests/fixtures/with_srs_3857.las")
    >>>
    >>> convert(
    ...     las_path, # the Path to the file to convert, it can be a list of Path
    ...     outfolder=Path("3dtiles_output/"),
    ...     crs_out=CRS.from_epsg(4978),
    ...     jobs=2,
    ...     verbose=-1
    ... )
    >>>
