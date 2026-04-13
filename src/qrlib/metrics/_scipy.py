"""基于 SciPy KDTree 的 numpy 快路径。"""

from __future__ import annotations

import numpy as np

try:
    from scipy.spatial import KDTree as _KDTree
except ImportError:  # pragma: no cover - SciPy 为可选依赖
    _KDTree = None

__all__ = [
    "SCIPY_AVAILABLE",
    "directional_nearest_neighbor_distances",
]

SCIPY_AVAILABLE = _KDTree is not None


def directional_nearest_neighbor_distances(
    source: np.ndarray,
    target: np.ndarray,
    *,
    norm: str,
) -> np.ndarray:
    """按 batch 样本计算 source 到 target 的最近邻距离。"""

    if _KDTree is None:  # pragma: no cover - 调用方会先判断可用性
        raise RuntimeError("SciPy KDTree is not available")

    p = 1 if norm == "l1" else 2
    batch_shape = source.shape[:-2]
    flat_source = source.reshape(-1, source.shape[-2], source.shape[-1])
    flat_target = target.reshape(-1, target.shape[-2], target.shape[-1])
    flat_distances = np.empty((flat_source.shape[0], source.shape[-2]), dtype=source.dtype)

    for index, (source_points, target_points) in enumerate(
        zip(flat_source, flat_target, strict=True)
    ):
        tree = _KDTree(target_points)
        distances, _ = tree.query(source_points, k=1, p=p, workers=1)
        flat_distances[index] = np.asarray(distances, dtype=source.dtype)

    return flat_distances.reshape((*batch_shape, source.shape[-2]))
