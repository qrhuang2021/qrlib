"""几何数据模型。"""

from __future__ import annotations

from dataclasses import dataclass

from ._typing import ArrayLike, FaceArrayLike, ScaleLike, VectorLike
from ._validation import ensure_same_backend, validate_face_array, validate_points_array

__all__ = ["Mesh", "PointCloud"]


@dataclass(frozen=True, slots=True)
class PointCloud:
    """点云坐标容器。"""

    points: ArrayLike

    def __post_init__(self) -> None:
        validate_points_array(self.points, name="points")

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
        validate_points_array(self.vertices, name="vertices")
        validate_face_array(self.faces, name="faces")
        ensure_same_backend(
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
