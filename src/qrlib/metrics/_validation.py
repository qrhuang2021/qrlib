"""指标输入校验与模式校验。"""

from __future__ import annotations

from qrlib.geometry import PointCloud

import numpy as np

from ._typing import ArrayLike, MetricInput

try:
    import torch as _torch
except ImportError:  # pragma: no cover - 运行时允许无 torch 环境
    _torch = None

__all__ = [
    "ensure_same_backend",
    "is_torch_array",
    "unwrap_metric_input",
    "validate_bidirectional_reduction",
    "validate_matching_batch_shape",
    "validate_norm",
    "validate_points_array",
    "validate_reduction",
]


def is_torch_array(value: object) -> bool:
    """判断输入是否为 torch 张量。"""

    return _torch is not None and isinstance(value, _torch.Tensor)


def validate_points_array(points: ArrayLike, *, name: str) -> None:
    """校验点坐标数组形状。"""

    if not isinstance(points, np.ndarray) and not is_torch_array(points):
        raise TypeError(f"{name} must be a numpy.ndarray, torch.Tensor, or PointCloud")
    if points.ndim < 2 or points.shape[-1] != 3:
        raise ValueError(f"{name} must have shape (N, 3) or (..., N, 3)")
    if points.shape[-2] == 0:
        raise ValueError(f"{name} must contain at least one point")


def unwrap_metric_input(value: MetricInput, *, name: str) -> ArrayLike:
    """把 PointCloud 或数组统一解包为点坐标。"""

    points = value.points if isinstance(value, PointCloud) else value
    validate_points_array(points, name=name)
    return points


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


def validate_matching_batch_shape(source: ArrayLike, target: ArrayLike) -> None:
    """确保 source 与 target 具有完全一致的 batch 前缀。"""

    if source.shape[:-2] != target.shape[:-2]:
        raise ValueError("source and target must share the same batch shape")


def validate_norm(norm: str) -> None:
    """校验范数字符串。"""

    if norm not in {"l1", "l2"}:
        raise ValueError("norm must be 'l1' or 'l2'")


def validate_reduction(reduction: str) -> None:
    """校验 batch 归约模式。"""

    if reduction not in {"none", "mean"}:
        raise ValueError("reduction must be 'none' or 'mean'")


def validate_bidirectional_reduction(reduction: str) -> None:
    """校验双向 Chamfer 聚合模式。"""

    if reduction not in {"sum", "mean"}:
        raise ValueError("bidirectional_reduction must be 'sum' or 'mean'")
