"""几何数据类型定义。"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeAlias

import numpy as np

try:
    import torch as _torch
except ImportError:  # pragma: no cover - 运行时允许无 torch 环境
    _torch = None

if TYPE_CHECKING:
    import torch

    TorchTensor: TypeAlias = torch.Tensor
else:
    if _torch is None:

        class TorchTensor:  # pragma: no cover - 只为运行时类型别名占位
            """torch.Tensor 缺失时的占位类型。"""

    else:
        TorchTensor = _torch.Tensor

ArrayLike: TypeAlias = np.ndarray | TorchTensor
FaceArrayLike: TypeAlias = ArrayLike
VectorLike: TypeAlias = ArrayLike | Sequence[float]
ScaleLike: TypeAlias = ArrayLike | float

__all__ = [
    "ArrayLike",
    "FaceArrayLike",
    "VectorLike",
    "ScaleLike",
    "PointCloud",
    "Mesh",
]


class _GeometryValidator:
    """统一处理几何输入的基础校验。"""

    def is_torch_array(self, value: object) -> bool:
        return _torch is not None and isinstance(value, _torch.Tensor)

    def is_supported_array(self, value: object) -> bool:
        return isinstance(value, np.ndarray) or self.is_torch_array(value)

    def validate_points(self, points: ArrayLike, *, name: str) -> None:
        if not self.is_supported_array(points):
            raise TypeError(f"{name} must be a numpy.ndarray or torch.Tensor")
        if points.ndim < 2 or points.shape[-1] != 3:
            raise ValueError(f"{name} must have shape (N, 3) or (..., N, 3)")

    def validate_faces(self, faces: FaceArrayLike, *, name: str) -> None:
        if not self.is_supported_array(faces):
            raise TypeError(f"{name} must be a numpy.ndarray or torch.Tensor")
        if faces.ndim != 2 or faces.shape[-1] < 3:
            raise ValueError(f"{name} must have shape (F, K), and K must be >= 3")
        if self.is_torch_array(faces):
            if faces.dtype not in {
                _torch.int8,
                _torch.int16,
                _torch.int32,
                _torch.int64,
                _torch.uint8,
            }:
                raise ValueError(f"{name} must use an integer dtype")
            return

        if not np.issubdtype(faces.dtype, np.integer):
            raise ValueError(f"{name} must use an integer dtype")

    def ensure_same_backend(
        self,
        first: ArrayLike,
        second: ArrayLike,
        *,
        first_name: str,
        second_name: str,
    ) -> None:
        if self.is_torch_array(first) != self.is_torch_array(second):
            raise TypeError(f"{first_name} and {second_name} must use the same backend family")


_GEOMETRY_VALIDATOR = _GeometryValidator()


def _is_torch_array(value: object) -> bool:
    return _GEOMETRY_VALIDATOR.is_torch_array(value)


def _validate_points_array(points: ArrayLike, *, name: str) -> None:
    _GEOMETRY_VALIDATOR.validate_points(points, name=name)


def _validate_face_array(faces: FaceArrayLike, *, name: str) -> None:
    _GEOMETRY_VALIDATOR.validate_faces(faces, name=name)


def _ensure_same_backend(
    first: ArrayLike,
    second: ArrayLike,
    *,
    first_name: str,
    second_name: str,
) -> None:
    _GEOMETRY_VALIDATOR.ensure_same_backend(
        first,
        second,
        first_name=first_name,
        second_name=second_name,
    )


@dataclass(frozen=True, slots=True)
class PointCloud:
    """点云坐标容器。"""

    points: ArrayLike

    def __post_init__(self) -> None:
        _validate_points_array(self.points, name="points")

    def normalize_to_sphere(
        self,
        center: VectorLike = (0.0, 0.0, 0.0),
        radius: ScaleLike = 1.0,
        eps: float = 1e-8,
    ) -> tuple[PointCloud, ArrayLike, ArrayLike]:
        from .normalization import normalize_to_sphere

        return normalize_to_sphere(self, center=center, radius=radius, eps=eps)

    def normalize_to_cube(
        self,
        center: VectorLike = (0.0, 0.0, 0.0),
        edge_length: ScaleLike = 2.0,
        eps: float = 1e-8,
    ) -> tuple[PointCloud, ArrayLike, ArrayLike]:
        from .normalization import normalize_to_cube

        return normalize_to_cube(self, center=center, edge_length=edge_length, eps=eps)

    def normalize(
        self,
        center: VectorLike,
        scale: ScaleLike,
        eps: float = 1e-8,
    ) -> PointCloud:
        from .normalization import normalize

        return normalize(self, center=center, scale=scale, eps=eps)

    def denormalize(
        self,
        center: VectorLike,
        scale: ScaleLike,
        eps: float = 1e-8,
    ) -> PointCloud:
        from .normalization import denormalize

        return denormalize(self, center=center, scale=scale, eps=eps)


@dataclass(frozen=True, slots=True)
class Mesh:
    """网格顶点与面索引容器。"""

    vertices: ArrayLike
    faces: FaceArrayLike

    def __post_init__(self) -> None:
        _validate_points_array(self.vertices, name="vertices")
        _validate_face_array(self.faces, name="faces")
        _ensure_same_backend(
            self.vertices,
            self.faces,
            first_name="vertices",
            second_name="faces",
        )

    def normalize_to_sphere(
        self,
        center: VectorLike = (0.0, 0.0, 0.0),
        radius: ScaleLike = 1.0,
        eps: float = 1e-8,
    ) -> tuple[Mesh, ArrayLike, ArrayLike]:
        from .normalization import normalize_to_sphere

        return normalize_to_sphere(self, center=center, radius=radius, eps=eps)

    def normalize_to_cube(
        self,
        center: VectorLike = (0.0, 0.0, 0.0),
        edge_length: ScaleLike = 2.0,
        eps: float = 1e-8,
    ) -> tuple[Mesh, ArrayLike, ArrayLike]:
        from .normalization import normalize_to_cube

        return normalize_to_cube(self, center=center, edge_length=edge_length, eps=eps)

    def normalize(
        self,
        center: VectorLike,
        scale: ScaleLike,
        eps: float = 1e-8,
    ) -> Mesh:
        from .normalization import normalize

        return normalize(self, center=center, scale=scale, eps=eps)

    def denormalize(
        self,
        center: VectorLike,
        scale: ScaleLike,
        eps: float = 1e-8,
    ) -> Mesh:
        from .normalization import denormalize

        return denormalize(self, center=center, scale=scale, eps=eps)
