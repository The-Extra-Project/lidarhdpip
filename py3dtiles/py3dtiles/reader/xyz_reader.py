import math
from pathlib import Path
from typing import Generator, List, Optional, Tuple

import numpy as np
import numpy.typing as npt
from pyproj import Transformer

from py3dtiles.typing import MetadataReaderType, OffsetScaleType, PortionItemType


def get_metadata(path: Path, fraction: int = 100) -> MetadataReaderType:
    aabb = None
    count = 0
    seek_values = []

    with path.open() as f:
        while True:
            batch = 10_000
            points = np.zeros((batch, 3))

            offset = f.tell()
            for i in range(batch):
                line = f.readline()
                if not line:
                    points = np.resize(points, (i, 3))
                    break
                points[i] = [float(s) for s in line.split(" ")][:3]

            if points.shape[0] == 0:
                break

            if not count % 1_000_000:
                seek_values += [offset]

            count += points.shape[0]
            batch_aabb = np.array([np.min(points, axis=0), np.max(points, axis=0)])

            # Update aabb
            if aabb is None:
                aabb = batch_aabb
            else:
                aabb[0] = np.minimum(aabb[0], batch_aabb[0])
                aabb[1] = np.maximum(aabb[1], batch_aabb[1])

        # We need an exact point count
        point_count = count * fraction // 100

        _1M = min(count, 1_000_000)
        steps = math.ceil(count / _1M)
        if steps != len(seek_values):
            raise ValueError(
                "the size of seek_values should be equal to steps,"
                f"currently steps = {steps} and len(seek_values) = {len(seek_values)}"
            )
        portions: List[PortionItemType] = [
            (i * _1M, min(count, (i + 1) * _1M), seek_values[i]) for i in range(steps)
        ]

        pointcloud_file_portions = [(str(path), p) for p in portions]

    if aabb is None:
        raise ValueError(f"There is no point in the file {path}")

    return {
        "portions": pointcloud_file_portions,
        "aabb": aabb,
        "crs_in": None,
        "point_count": point_count,
        "avg_min": aabb[0],
    }


def run(
    filename: str,
    offset_scale: OffsetScaleType,
    portion: PortionItemType,
    transformer: Optional[Transformer],
    color_scale: Optional[float],
) -> Generator[
    Tuple[npt.NDArray[np.float32], npt.NDArray[np.uint8], npt.NDArray[np.uint8]],
    None,
    None,
]:
    """
    Reads points from a xyz file

    Consider XYZIRGB format following FME documentation(*). If the number of
    features does not correspond (i.e. does not equal to 7), we do the
    following hypothesis:
    - 3 features mean XYZ
    - 4 features mean XYZI
    - 6 features mean XYZRGB

    NOTE: we assume RGB are 8 bits components.

    (*) See: https://docs.safe.com/fme/html/FME_Desktop_Documentation/FME_ReadersWriters/pointcloudxyz/pointcloudxyz.htm
    """
    with open(filename) as f:

        point_count = portion[1] - portion[0]

        step = min(point_count, max((point_count) // 10, 100000))

        f.seek(portion[2])

        feature_nb = 7

        for _ in range(0, point_count, step):
            points = np.zeros((step, feature_nb), dtype=np.float32)

            for j in range(step):
                line = f.readline()
                if not line:
                    points = np.resize(points, (j, feature_nb))
                    break
                line_features: List[float | None] = [float(s) for s in line.split(" ")]
                if len(line_features) == 3:
                    line_features += [None] * 4  # Insert intensity and RGB
                elif len(line_features) == 4:
                    line_features += [None] * 3  # Insert RGB
                elif len(line_features) == 6:
                    line_features.insert(3, None)  # Insert intensity
                points[j] = line_features

            x, y, z = (points[:, c] for c in [0, 1, 2])

            if transformer:
                x, y, z = transformer.transform(x, y, z)

            x = (x + offset_scale[0][0]) * offset_scale[1][0]
            y = (y + offset_scale[0][1]) * offset_scale[1][1]
            z = (z + offset_scale[0][2]) * offset_scale[1][2]

            coords = np.vstack((x, y, z)).transpose()

            if offset_scale[2] is not None:
                # Apply transformation matrix (because the tile's transform will contain
                # the inverse of this matrix)
                coords = np.dot(coords, offset_scale[2])

            coords = np.ascontiguousarray(coords.astype(np.float32))

            # Read colors: 3 last columns of the point cloud
            if color_scale is None:
                colors = points[:, -3:].astype(np.uint8)
            else:
                colors = np.clip(points[:, -3:] * color_scale, 0, 255).astype(np.uint8)

            classification = np.zeros((points.shape[0], 1), dtype=np.uint8)

            yield coords, colors, classification
