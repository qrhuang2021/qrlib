"""几何归一化与反归一化接口。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import overload

from ._backend import backend
from ._models import Mesh, PointCloud
from ._typing import ArrayLike, ScaleLike, VectorLike
from ._validation import validate_points_array

__all__ = [
    "normalize_to_sphere",
    "normalize_to_cube",
    "normalize",
    "denormalize",
]


@dataclass(frozen=True, slots=True)
class _GeometryPayload:
    """记录输入几何的载体信息，用于重建输出。"""

    kind: str
    coordinates: ArrayLike
    faces: ArrayLike | None = None


class _GeometryAdapter:
    """在数组、点云与网格之间做统一适配。"""

    def unwrap(self, data: ArrayLike | PointCloud | Mesh) -> _GeometryPayload:
        if isinstance(data, PointCloud):
            return _GeometryPayload(kind="point_cloud", coordinates=data.points)
        if isinstance(data, Mesh):
            return _GeometryPayload(kind="mesh", coordinates=data.vertices, faces=data.faces)

        validate_points_array(data, name="data")
        return _GeometryPayload(kind="array", coordinates=data)

    def rebuild(
        self,
        payload: _GeometryPayload,
        coordinates: ArrayLike,
    ) -> ArrayLike | PointCloud | Mesh:
        if payload.kind == "point_cloud":
            return PointCloud(coordinates)
        if payload.kind == "mesh":
            return Mesh(vertices=coordinates, faces=payload.faces)
        return coordinates


geometry_adapter = _GeometryAdapter()


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

    payload = geometry_adapter.unwrap(data)
    points = backend.to_coordinate_array(payload.coordinates)
    source_center = backend.mean_points(points)
    centered_points = backend.subtract_points(points, source_center)
    source_scale = backend.clamp_minimum(backend.max_point_radius(centered_points), eps)
    unit_points = backend.divide_points(centered_points, source_scale)

    target_center = backend.to_parameter_array(center, like=points)
    target_radius = backend.to_parameter_array(radius, like=points)
    backend.ensure_minimum(target_radius, eps, name="radius")

    normalized_points = backend.multiply_points(unit_points, target_radius)
    normalized_points = backend.add_points(normalized_points, target_center)
    return geometry_adapter.rebuild(payload, normalized_points), source_center, source_scale


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

    payload = geometry_adapter.unwrap(data)
    points = backend.to_coordinate_array(payload.coordinates)
    source_center, source_scale = backend.bbox_center_and_scale(points)
    source_scale = backend.clamp_minimum(source_scale, eps)
    unit_points = backend.divide_points(
        backend.subtract_points(points, source_center), source_scale
    )

    target_center = backend.to_parameter_array(center, like=points)
    target_edge_length = backend.to_parameter_array(edge_length, like=points)
    backend.ensure_minimum(target_edge_length, 2 * eps, name="edge_length")
    target_scale = target_edge_length / 2

    normalized_points = backend.multiply_points(unit_points, target_scale)
    normalized_points = backend.add_points(normalized_points, target_center)
    return geometry_adapter.rebuild(payload, normalized_points), source_center, source_scale


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

    payload = geometry_adapter.unwrap(data)
    points = backend.to_coordinate_array(payload.coordinates)
    target_center = backend.to_parameter_array(center, like=points)
    target_scale = backend.to_parameter_array(scale, like=points)
    backend.ensure_minimum(target_scale, eps, name="scale")

    normalized_points = backend.subtract_points(points, target_center)
    normalized_points = backend.divide_points(normalized_points, target_scale)
    return geometry_adapter.rebuild(payload, normalized_points)


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

    payload = geometry_adapter.unwrap(data)
    points = backend.to_coordinate_array(payload.coordinates)
    target_center = backend.to_parameter_array(center, like=points)
    target_scale = backend.to_parameter_array(scale, like=points)
    backend.ensure_minimum(target_scale, eps, name="scale")

    denormalized_points = backend.multiply_points(points, target_scale)
    denormalized_points = backend.add_points(denormalized_points, target_center)
    return geometry_adapter.rebuild(payload, denormalized_points)
