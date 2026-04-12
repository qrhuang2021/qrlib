"""几何归一化与反归一化接口。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import overload

import numpy as np

from .types import (
    ArrayLike,
    Mesh,
    PointCloud,
    ScaleLike,
    VectorLike,
    _is_torch_array,
    _validate_points_array,
)

try:
    import torch as _torch
except ImportError:  # pragma: no cover - 运行时允许无 torch 环境
    _torch = None

__all__ = [
    "normalize_to_sphere",
    "normalize_to_cube",
    "normalize",
    "denormalize",
]


class _BackendAdapter:
    """封装 numpy / torch 的基础张量运算。"""

    def to_coordinate_array(self, value: ArrayLike) -> ArrayLike:
        if _is_torch_array(value):
            return value if value.is_floating_point() else value.to(dtype=_torch.float32)
        return value if np.issubdtype(value.dtype, np.floating) else value.astype(np.float32)

    def to_parameter_array(
        self, value: VectorLike | ScaleLike | float, *, like: ArrayLike
    ) -> ArrayLike:
        if _is_torch_array(like):
            if _is_torch_array(value):
                return value.to(device=like.device, dtype=like.dtype)
            return _torch.as_tensor(value, device=like.device, dtype=like.dtype)

        if _is_torch_array(value):
            value = value.detach().cpu().numpy()
        return np.asarray(value, dtype=like.dtype)

    def ensure_minimum(self, value: ArrayLike, minimum: float, *, name: str) -> None:
        if _is_torch_array(value):
            lower_bound = _torch.as_tensor(minimum, dtype=value.dtype, device=value.device)
            if bool(_torch.any(value < lower_bound)):
                raise ValueError(f"{name} must be >= {minimum}")
            return

        lower_bound = np.asarray(minimum, dtype=value.dtype)
        if np.any(value < lower_bound):
            raise ValueError(f"{name} must be >= {minimum}")

    def mean_points(self, points: ArrayLike) -> ArrayLike:
        return points.mean(dim=-2) if _is_torch_array(points) else points.mean(axis=-2)

    def max_point_radius(self, centered_points: ArrayLike) -> ArrayLike:
        if _is_torch_array(centered_points):
            return _torch.linalg.norm(centered_points, dim=-1).amax(dim=-1)
        return np.linalg.norm(centered_points, axis=-1).max(axis=-1)

    def bbox_center_and_scale(self, points: ArrayLike) -> tuple[ArrayLike, ArrayLike]:
        if _is_torch_array(points):
            mins = points.amin(dim=-2)
            maxs = points.amax(dim=-2)
            center = (mins + maxs) / 2
            scale = ((maxs - mins) / 2).amax(dim=-1)
            return center, scale

        mins = points.min(axis=-2)
        maxs = points.max(axis=-2)
        center = (mins + maxs) / 2
        scale = ((maxs - mins) / 2).max(axis=-1)
        return center, scale

    def clamp_minimum(self, value: ArrayLike, minimum: float) -> ArrayLike:
        if _is_torch_array(value):
            lower_bound = _torch.as_tensor(minimum, dtype=value.dtype, device=value.device)
            return _torch.clamp(value, min=lower_bound)
        return np.maximum(value, np.asarray(minimum, dtype=value.dtype))

    def subtract_points(self, points: ArrayLike, center: ArrayLike) -> ArrayLike:
        try:
            return points - self._expand_center_like_points(center, points)
        except Exception as error:  # noqa: BLE001
            raise ValueError(
                "center must be broadcastable to point coordinates as (3,) or (..., 3)"
            ) from error

    def add_points(self, points: ArrayLike, center: ArrayLike) -> ArrayLike:
        try:
            return points + self._expand_center_like_points(center, points)
        except Exception as error:  # noqa: BLE001
            raise ValueError(
                "center must be broadcastable to point coordinates as (3,) or (..., 3)"
            ) from error

    def divide_points(self, points: ArrayLike, scale: ArrayLike) -> ArrayLike:
        try:
            return points / self._expand_scale_like_points(scale, points)
        except Exception as error:  # noqa: BLE001
            raise ValueError(
                "scale must be a scalar or broadcastable to the batch shape of coordinates"
            ) from error

    def multiply_points(self, points: ArrayLike, scale: ArrayLike) -> ArrayLike:
        try:
            return points * self._expand_scale_like_points(scale, points)
        except Exception as error:  # noqa: BLE001
            raise ValueError(
                "scale must be a scalar or broadcastable to the batch shape of coordinates"
            ) from error

    def _expand_center_like_points(self, center: ArrayLike, points: ArrayLike) -> ArrayLike:
        if center.ndim == 1:
            return center
        if center.ndim == points.ndim - 1:
            return center[..., None, :]
        return center

    def _expand_scale_like_points(self, scale: ArrayLike, points: ArrayLike) -> ArrayLike:
        expanded_scale = scale
        while expanded_scale.ndim < points.ndim:
            expanded_scale = expanded_scale[..., None]
        return expanded_scale


@dataclass(frozen=True, slots=True)
class _GeometryPayload:
    """记录输入几何的载体信息，用于重建输出。"""

    kind: str
    coordinates: ArrayLike
    faces: ArrayLike | None = None


class _GeometryAdapter:
    """在原始数组、点云与网格之间做统一适配。"""

    def unwrap(self, data: ArrayLike | PointCloud | Mesh) -> _GeometryPayload:
        if isinstance(data, PointCloud):
            return _GeometryPayload(kind="point_cloud", coordinates=data.points)
        if isinstance(data, Mesh):
            return _GeometryPayload(kind="mesh", coordinates=data.vertices, faces=data.faces)

        _validate_points_array(data, name="data")
        return _GeometryPayload(kind="array", coordinates=data)

    def rebuild(
        self, payload: _GeometryPayload, coordinates: ArrayLike
    ) -> ArrayLike | PointCloud | Mesh:
        if payload.kind == "point_cloud":
            return PointCloud(coordinates)
        if payload.kind == "mesh":
            return Mesh(vertices=coordinates, faces=payload.faces)
        return coordinates


_BACKEND = _BackendAdapter()
_GEOMETRY = _GeometryAdapter()


@overload
def normalize_to_sphere(
    data: ArrayLike,
    center: VectorLike = (0.0, 0.0, 0.0),
    radius: ScaleLike = 1.0,
    eps: float = 1e-8,
) -> tuple[ArrayLike, ArrayLike, ArrayLike]: ...


@overload
def normalize_to_sphere(
    data: PointCloud,
    center: VectorLike = (0.0, 0.0, 0.0),
    radius: ScaleLike = 1.0,
    eps: float = 1e-8,
) -> tuple[PointCloud, ArrayLike, ArrayLike]: ...


@overload
def normalize_to_sphere(
    data: Mesh,
    center: VectorLike = (0.0, 0.0, 0.0),
    radius: ScaleLike = 1.0,
    eps: float = 1e-8,
) -> tuple[Mesh, ArrayLike, ArrayLike]: ...


def normalize_to_sphere(
    data: ArrayLike | PointCloud | Mesh,
    center: VectorLike = (0.0, 0.0, 0.0),
    radius: ScaleLike = 1.0,
    eps: float = 1e-8,
) -> tuple[ArrayLike | PointCloud | Mesh, ArrayLike, ArrayLike]:
    """把几何数据归一化到目标球内，并返回源中心与源尺度。"""

    payload = _GEOMETRY.unwrap(data)
    points = _BACKEND.to_coordinate_array(payload.coordinates)
    source_center = _BACKEND.mean_points(points)
    centered_points = _BACKEND.subtract_points(points, source_center)
    source_scale = _BACKEND.clamp_minimum(_BACKEND.max_point_radius(centered_points), eps)
    unit_points = _BACKEND.divide_points(centered_points, source_scale)

    target_center = _BACKEND.to_parameter_array(center, like=points)
    target_radius = _BACKEND.to_parameter_array(radius, like=points)
    _BACKEND.ensure_minimum(target_radius, eps, name="radius")

    normalized_points = _BACKEND.multiply_points(unit_points, target_radius)
    normalized_points = _BACKEND.add_points(normalized_points, target_center)
    return _GEOMETRY.rebuild(payload, normalized_points), source_center, source_scale


@overload
def normalize_to_cube(
    data: ArrayLike,
    center: VectorLike = (0.0, 0.0, 0.0),
    edge_length: ScaleLike = 2.0,
    eps: float = 1e-8,
) -> tuple[ArrayLike, ArrayLike, ArrayLike]: ...


@overload
def normalize_to_cube(
    data: PointCloud,
    center: VectorLike = (0.0, 0.0, 0.0),
    edge_length: ScaleLike = 2.0,
    eps: float = 1e-8,
) -> tuple[PointCloud, ArrayLike, ArrayLike]: ...


@overload
def normalize_to_cube(
    data: Mesh,
    center: VectorLike = (0.0, 0.0, 0.0),
    edge_length: ScaleLike = 2.0,
    eps: float = 1e-8,
) -> tuple[Mesh, ArrayLike, ArrayLike]: ...


def normalize_to_cube(
    data: ArrayLike | PointCloud | Mesh,
    center: VectorLike = (0.0, 0.0, 0.0),
    edge_length: ScaleLike = 2.0,
    eps: float = 1e-8,
) -> tuple[ArrayLike | PointCloud | Mesh, ArrayLike, ArrayLike]:
    """把几何数据归一化到目标立方体内，并返回源中心与源尺度。"""

    payload = _GEOMETRY.unwrap(data)
    points = _BACKEND.to_coordinate_array(payload.coordinates)
    source_center, source_scale = _BACKEND.bbox_center_and_scale(points)
    source_scale = _BACKEND.clamp_minimum(source_scale, eps)
    unit_points = _BACKEND.divide_points(
        _BACKEND.subtract_points(points, source_center), source_scale
    )

    target_center = _BACKEND.to_parameter_array(center, like=points)
    target_edge_length = _BACKEND.to_parameter_array(edge_length, like=points)
    _BACKEND.ensure_minimum(target_edge_length, 2 * eps, name="edge_length")
    target_scale = target_edge_length / 2

    normalized_points = _BACKEND.multiply_points(unit_points, target_scale)
    normalized_points = _BACKEND.add_points(normalized_points, target_center)
    return _GEOMETRY.rebuild(payload, normalized_points), source_center, source_scale


@overload
def normalize(
    data: ArrayLike,
    center: VectorLike,
    scale: ScaleLike,
    eps: float = 1e-8,
) -> ArrayLike: ...


@overload
def normalize(
    data: PointCloud,
    center: VectorLike,
    scale: ScaleLike,
    eps: float = 1e-8,
) -> PointCloud: ...


@overload
def normalize(
    data: Mesh,
    center: VectorLike,
    scale: ScaleLike,
    eps: float = 1e-8,
) -> Mesh: ...


def normalize(
    data: ArrayLike | PointCloud | Mesh,
    center: VectorLike,
    scale: ScaleLike,
    eps: float = 1e-8,
) -> ArrayLike | PointCloud | Mesh:
    """使用显式 center / scale 对几何数据做归一化。"""

    payload = _GEOMETRY.unwrap(data)
    points = _BACKEND.to_coordinate_array(payload.coordinates)
    target_center = _BACKEND.to_parameter_array(center, like=points)
    target_scale = _BACKEND.to_parameter_array(scale, like=points)
    _BACKEND.ensure_minimum(target_scale, eps, name="scale")

    normalized_points = _BACKEND.subtract_points(points, target_center)
    normalized_points = _BACKEND.divide_points(normalized_points, target_scale)
    return _GEOMETRY.rebuild(payload, normalized_points)


@overload
def denormalize(
    data: ArrayLike,
    center: VectorLike,
    scale: ScaleLike,
    eps: float = 1e-8,
) -> ArrayLike: ...


@overload
def denormalize(
    data: PointCloud,
    center: VectorLike,
    scale: ScaleLike,
    eps: float = 1e-8,
) -> PointCloud: ...


@overload
def denormalize(
    data: Mesh,
    center: VectorLike,
    scale: ScaleLike,
    eps: float = 1e-8,
) -> Mesh: ...


def denormalize(
    data: ArrayLike | PointCloud | Mesh,
    center: VectorLike,
    scale: ScaleLike,
    eps: float = 1e-8,
) -> ArrayLike | PointCloud | Mesh:
    """使用显式 center / scale 把几何数据还原到原坐标系。"""

    payload = _GEOMETRY.unwrap(data)
    points = _BACKEND.to_coordinate_array(payload.coordinates)
    target_center = _BACKEND.to_parameter_array(center, like=points)
    target_scale = _BACKEND.to_parameter_array(scale, like=points)
    _BACKEND.ensure_minimum(target_scale, eps, name="scale")

    denormalized_points = _BACKEND.multiply_points(points, target_scale)
    denormalized_points = _BACKEND.add_points(denormalized_points, target_center)
    return _GEOMETRY.rebuild(payload, denormalized_points)
