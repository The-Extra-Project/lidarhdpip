# Changelog

All notable changes to this project will be documented in this file.

## v5.0.0 (2023-02-02)

### BREAKING CHANGE

- py3dtiles no longer support python 3.7 (it reaches EOL in june)
- The function convert_to_ecef has been removed
- Many imports have been changed, please update them accordingly:
    - `from py3dtiles import B3dm` becomes `from py3dtiles.tileset.content import B3dm`
    - `from py3dtiles import GlTF` becomes `from py3dtiles.tileset.content import GlTF`
    - `from py3dtiles import Pnts` becomes `from py3dtiles.tileset.content import Pnts`
    - `from py3dtiles import BatchTable` becomes `from py3dtiles.tileset.batch_table import BatchTable`
    - `from py3dtiles import BoundingVolumeBox` becomes `from py3dtiles.tileset.bounding_volume_box import BoundingVolumeBox`
    - `from py3dtiles import Extendable` becomes `from py3dtiles.tileset.extendable import Extendable`
    - `from py3dtiles import Extension` becomes `from py3dtiles.tileset.extension import BaseExtension`
    - `from py3dtiles import Tile` becomes `from py3dtiles.tileset.tile import Tile`
    - `from py3dtiles import TileContent` becomes `from py3dtiles.tileset.tile_content import TileContent`
    - `from py3dtiles import TileSet` becomes `from py3dtiles.tileset.tileset import TileSet`
    - `from py3dtiles import TileContentReader` becomes `from py3dtiles.tileset.utils import TileContentReader`
    - `from py3dtiles import TriangleSoup` becomes `from py3dtiles.tilers.b3dm.wkb_utils import TriangleSoup`
    - `from py3dtiles import Feature` becomes `from py3dtiles.tileset.feature_table import Feature`
- The BoundingVolume class become an abstract class
- The way of getting / setting `transform` has changed:
    - The methods `set_transform` and `get_transform` of the class `Tile` has been removed, and the attribute `transform` of the class `Tile` has been renamed from `_transform` to `transform.` Please use the attribute directly.
    - in the same vein, the method `set_transform` of the class `Tileset` has been removed
    - The method set_from_array from the class BoundingVolumeBox has been removed, use set_from_list instead (with an ArrayLike)
- some parameters types have been set to always be a flat numpy array of `np.float64`:
    - `Tile.transform`
    - The parameter `offset` of the method `BoundingVolumeBox.translate`
    - The parameter `transform` of the method `BoundingVolumeBox.transform`
    - The parameter `box_list` of the method `BoundingVolumeBox.set_from_list`
    - The parameter `mins_maxs` of the method `BoundingVolumeBox.get_box_array_from_mins_maxs`
    - The parameter `points` of the method `BoundingVolumeBox.get_box_array_from_point`

### Features

- **convert.py**: add parameter to ignore CRS mixin in input files
- add the import and export of batch table from pnts (only json)
- **reader/ply_reader.py**: support .ply files
- **typing.py**: create the tileset json structure with typing annotations


### Fixes

- add and update typing annotations to fix all mypy issues
- check magic value as bytes not str
- exclude B028 flake8 rule
- **node.py**: delete tile children when the tile root is moved in a sub tileset

### Refactor

- remove all asserts in source code
- select only used fonctions from transformation file and update the code
- **LICENSE**: remove Mapbox third party license
- remove copied earcut code and use mapbox library
- change file hierarchy


## v4.0.0 (2023-01-09)

### BREAKING CHANGE

- The parameter `srs_in` and `srs_out` of `py3dtiles.convert.convert` have been
renamed to `crs_in` and `crs_out`. Furthermore, their type is no longer int
or str but `pyproj.CRS`. No change has been made to the command-line `py3dtiles convert`, but you can use proj4 string in addition to epsg code. To migrate old code, instead of:
```python
from py3dtiles.convert import convert
# ...
convert('without_srs.las', outfolder=tmp_dir, crs_out='4978')
```
you can do:
```python
from pyproj import CRS
from py3dtiles.convert import convert
# ...
convert('without_srs.las', outfolder=tmp_dir, crs_out=CRS.from_epsg(4978))
```
- SrsInMissingException has been moved from `py3dtiles/utils.py` to `py3dtiles/exceptions.py`.

### Feat

The main feature of this release is that you can now mix las/laz/xyz files in one invocation of the convert function.

### Fix

- **shared_node_store.py**: fix node removing in cache if already deleted
- change srs_in to srs_out to fix refactoring error
- avoid duplicate points when the mode is replace

### Refactor

- **convert**: rename the 'infos' variable and function to 'file_info'
- **convert**: use CRS almost everywhere instead of string representing epsg code
- **exceptions**: move all custom exceptions at the same place
- **convert**: use a dictionary to find the correct reader
- fix issues find by pre-commit

### Chores

- add pre-commit hooks

## v3.0.0

### BREAKING

Some renaming has been done to better follow the 3dtiles specification:

- `TileHeader` -> `TileContentHeader`
- `TileBody` -> `TileContentBody`
- The API of merger.py::merge wasn't really convenient to use and has now changed. Now the signature is:
```python3
def merge(folder: Union[str, Path], overwrite: bool = False, verbose: int = 0) -> None
```
- the argument verbose of the cli interface has changed. To increase the verbosity, the number of -v is counted (-vv will be a verbose of 2).
- Boolean options has been changed from `--foo=1` to simple flags: `--foo`. Affected options are `--overwrite` and `--graph`.
- `--rgb=no` has been replaced by a `--no-rgb` option to deactivate it. The default is still to keep color information

### Features

- support laz if laszip is installed
- windows support (NOTE: testers needed)
- Some classes to represent 3Dtiles concepts have been added:
	- BoundingVolumeBox
	- TileSet
	- Tile
	- uExtension

### Fix

- The geometric error of two merged tilesets is now the biggest of the two tileset geometric error divided by the ratio of kept points. We believe this use of GeometricError fits more the spirit of the specification.
- **node**: avoid empty children array in tileset.json
- **setup.py**: fix missing dependency pytest
- **node**: avoid to add empty children array
- disable padding if already 8-byte aligned instead of adding 8 new empty bytes
- **featureTable**: add a 8-byte boundary for FeatureTableBody
- **featureTable**: change the boundary from 4 to 8
- replace sys.exit(1) in convert by raising an exception

## v2.0.0

This releases completely reworks py3dtiles command line and add new features.

The command line now uses subcommands syntax, in order to expose a single
entry point and support multiple commands. The existing commands 'export_tileset' and 'py3dtiles_info' became
'py3dtiles export' and 'py3dtiles info'.

### Changes

- relicensed as Apache 2.0.
- minimal python supported is now 3.8
- dependencies versions has been updated:
    - laspy should be at least 2.0
    - numpy at least 1.20.0
- Tile has been renamed to TileContent

### Features

New features were added, the main one being: py3dtiles can be used to convert
pointcloud las files to a 3dtiles tileset.

This is the purpose of the 'py3dtiles convert' command. It supports multicore
processor for faster processing, leveraging pyzmq, and the memory management has been carefully
implemented to support virtually unlimited points count.

Other features:

- read points from xyz files
- Documentation are now published at https://oslandia.gitlab.io/py3dtiles

### Fixes

* 53580ba Jeremy Gaillard       fix: use y-up orientation for glTF objects in export script
* 65d6f67 Jeremy Gaillard       fix: proper bounding box size in export script
* 3603b00 Augustin Trancart     fix: reliably select triangulation projection plane and orientation
* fd2105a jailln                Fix gltf min and max value
