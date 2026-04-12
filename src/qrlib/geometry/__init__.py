"""几何数据类型与几何变换接口。"""

from .normalization import denormalize, normalize, normalize_to_cube, normalize_to_sphere
from .types import ArrayLike, FaceArrayLike, Mesh, PointCloud, ScaleLike, VectorLike

__all__ = [
    "ArrayLike",
    "FaceArrayLike",
    "ScaleLike",
    "VectorLike",
    "PointCloud",
    "Mesh",
    "normalize_to_sphere",
    "normalize_to_cube",
    "normalize",
    "denormalize",
]
