"""几何输入校验辅助函数。"""

from __future__ import annotations

import numpy as np

from ._typing import ArrayLike, FaceArrayLike

try:
    import torch as _torch
except ImportError:  # pragma: no cover - 运行时允许无 torch 环境
    _torch = None


__all__ = [
    "ensure_same_backend",
    "is_supported_array",
    "is_torch_array",
    "validate_face_array",
    "validate_points_array",
]


def is_torch_array(value: object) -> bool:
    """判断输入是否为 torch 张量。"""

    return _torch is not None and isinstance(value, _torch.Tensor)


def is_supported_array(value: object) -> bool:
    """判断输入是否属于受支持的数组后端。"""

    return isinstance(value, np.ndarray) or is_torch_array(value)


def validate_points_array(points: ArrayLike, *, name: str) -> None:
    """校验点坐标数组形状。"""

    if not is_supported_array(points):
        raise TypeError(f"{name} must be a numpy.ndarray or torch.Tensor")
    if points.ndim < 2 or points.shape[-1] != 3:
        raise ValueError(f"{name} must have shape (N, 3) or (..., N, 3)")


def validate_face_array(faces: FaceArrayLike, *, name: str) -> None:
    """校验网格面索引数组。"""

    if not is_supported_array(faces):
        raise TypeError(f"{name} must be a numpy.ndarray or torch.Tensor")
    if faces.ndim != 2 or faces.shape[-1] < 3:
        raise ValueError(f"{name} must have shape (F, K), and K must be >= 3")

    if is_torch_array(faces):
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
    first: ArrayLike,
    second: ArrayLike,
    *,
    first_name: str,
    second_name: str,
) -> None:
    """确保两个数组来自同一后端族。"""

    if is_torch_array(first) != is_torch_array(second):
        raise TypeError(f"{first_name} and {second_name} must use the same backend family")
