"""numpy / torch 的 dense 指标后端。"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ._typing import ArrayLike
from ._validation import is_torch_array

try:
    import torch as _torch
except ImportError:  # pragma: no cover - 运行时允许无 torch 环境
    _torch = None

__all__ = ["MetricsBackend", "backend"]


@dataclass(frozen=True, slots=True)
class MetricsBackend:
    """封装 numpy / torch 的 dense 距离计算。"""

    def to_coordinate_array(self, value: ArrayLike) -> ArrayLike:
        """把坐标转换为浮点数组。"""

        if is_torch_array(value):
            return value if value.is_floating_point() else value.to(dtype=_torch.float32)
        return value if np.issubdtype(value.dtype, np.floating) else value.astype(np.float32)

    def directional_nearest_neighbor_distances(
        self,
        source: ArrayLike,
        target: ArrayLike,
        *,
        norm: str,
    ) -> ArrayLike:
        """计算 source 中每个点到 target 的最近邻距离。"""

        pairwise_distances = self.pairwise_distances(source, target, norm=norm)
        if is_torch_array(pairwise_distances):
            return pairwise_distances.min(dim=-1).values
        return pairwise_distances.min(axis=-1)

    def pairwise_distances(
        self,
        source: ArrayLike,
        target: ArrayLike,
        *,
        norm: str,
    ) -> ArrayLike:
        """计算两组点之间的 dense pairwise 距离。"""

        differences = source[..., :, None, :] - target[..., None, :, :]
        if norm == "l1":
            return (
                differences.abs().sum(dim=-1)
                if is_torch_array(differences)
                else np.abs(differences).sum(axis=-1)
            )
        if is_torch_array(differences):
            return _torch.linalg.norm(differences, dim=-1)
        return np.linalg.norm(differences, axis=-1)

    def mean_over_points(self, values: ArrayLike) -> ArrayLike:
        """按点维求均值。"""

        return values.mean(dim=-1) if is_torch_array(values) else values.mean(axis=-1)

    def max_over_points(self, values: ArrayLike) -> ArrayLike:
        """按点维求最大值。"""

        return values.max(dim=-1).values if is_torch_array(values) else values.max(axis=-1)

    def mean_over_batch(self, values: ArrayLike) -> ArrayLike:
        """对 batch 结果求全局均值。"""

        return values.mean()

    def maximum(self, first: ArrayLike, second: ArrayLike) -> ArrayLike:
        """逐元素取最大值。"""

        if is_torch_array(first):
            return _torch.maximum(first, second)
        return np.maximum(first, second)


backend = MetricsBackend()
