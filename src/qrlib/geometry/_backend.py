"""numpy / torch 几何后端适配。"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ._typing import ArrayLike, ScaleLike, VectorLike
from ._validation import is_torch_array

try:
    import torch as _torch
except ImportError:  # pragma: no cover - 运行时允许无 torch 环境
    _torch = None

__all__ = ["BackendAdapter", "backend"]


@dataclass(frozen=True, slots=True)
class BackendAdapter:
    """封装 numpy / torch 的基础张量运算。"""

    def to_coordinate_array(self, value: ArrayLike) -> ArrayLike:
        """把坐标转换为浮点数组。"""

        if is_torch_array(value):
            return value if value.is_floating_point() else value.to(dtype=_torch.float32)
        return value if np.issubdtype(value.dtype, np.floating) else value.astype(np.float32)

    def to_parameter_array(
        self,
        value: VectorLike | ScaleLike | float,
        *,
        like: ArrayLike,
    ) -> ArrayLike:
        """把参数转换到与参考数组一致的后端与 dtype。"""

        if is_torch_array(like):
            if is_torch_array(value):
                return value.to(device=like.device, dtype=like.dtype)
            return _torch.as_tensor(value, device=like.device, dtype=like.dtype)

        if is_torch_array(value):
            value = value.detach().cpu().numpy()
        return np.asarray(value, dtype=like.dtype)

    def ensure_minimum(self, value: ArrayLike, minimum: float, *, name: str) -> None:
        """确保数值不低于最小阈值。"""

        if is_torch_array(value):
            lower_bound = _torch.as_tensor(minimum, dtype=value.dtype, device=value.device)
            if bool(_torch.any(value < lower_bound)):
                raise ValueError(f"{name} must be >= {minimum}")
            return

        lower_bound = np.asarray(minimum, dtype=value.dtype)
        if np.any(value < lower_bound):
            raise ValueError(f"{name} must be >= {minimum}")

    def mean_points(self, points: ArrayLike) -> ArrayLike:
        """计算点坐标均值中心。"""

        return points.mean(dim=-2) if is_torch_array(points) else points.mean(axis=-2)

    def max_point_radius(self, centered_points: ArrayLike) -> ArrayLike:
        """计算点集相对中心的最大欧氏距离。"""

        if is_torch_array(centered_points):
            return _torch.linalg.norm(centered_points, dim=-1).amax(dim=-1)
        return np.linalg.norm(centered_points, axis=-1).max(axis=-1)

    def bbox_center_and_scale(self, points: ArrayLike) -> tuple[ArrayLike, ArrayLike]:
        """计算包围盒中心与最大半边长。"""

        if is_torch_array(points):
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
        """把数值钳制到最小阈值以上。"""

        if is_torch_array(value):
            lower_bound = _torch.as_tensor(minimum, dtype=value.dtype, device=value.device)
            return _torch.clamp(value, min=lower_bound)
        return np.maximum(value, np.asarray(minimum, dtype=value.dtype))

    def subtract_points(self, points: ArrayLike, center: ArrayLike) -> ArrayLike:
        """按点坐标形状减去中心。"""

        try:
            return points - self._expand_center_like_points(center, points)
        except Exception as error:  # noqa: BLE001
            raise ValueError(
                "center must be broadcastable to point coordinates as (3,) or (..., 3)"
            ) from error

    def add_points(self, points: ArrayLike, center: ArrayLike) -> ArrayLike:
        """按点坐标形状加回中心。"""

        try:
            return points + self._expand_center_like_points(center, points)
        except Exception as error:  # noqa: BLE001
            raise ValueError(
                "center must be broadcastable to point coordinates as (3,) or (..., 3)"
            ) from error

    def divide_points(self, points: ArrayLike, scale: ArrayLike) -> ArrayLike:
        """按批次尺度对点坐标做除法。"""

        try:
            return points / self._expand_scale_like_points(scale, points)
        except Exception as error:  # noqa: BLE001
            raise ValueError(
                "scale must be a scalar or broadcastable to the batch shape of coordinates"
            ) from error

    def multiply_points(self, points: ArrayLike, scale: ArrayLike) -> ArrayLike:
        """按批次尺度对点坐标做乘法。"""

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


backend = BackendAdapter()
