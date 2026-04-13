"""公开的点云距离指标接口。"""

from __future__ import annotations

import numpy as np

from ._backend import backend
from ._scipy import (
    SCIPY_AVAILABLE,
    directional_nearest_neighbor_distances as scipy_directional_distances,
)
from ._typing import ArrayLike, MetricInput
from ._validation import (
    ensure_same_backend,
    unwrap_metric_input,
    validate_bidirectional_reduction,
    validate_matching_batch_shape,
    validate_norm,
    validate_reduction,
)

__all__ = ["chamfer_distance", "hausdorff_distance"]


def _directional_nearest_neighbor_distances(
    source: ArrayLike,
    target: ArrayLike,
    *,
    norm: str,
) -> ArrayLike:
    if isinstance(source, np.ndarray) and SCIPY_AVAILABLE:
        return scipy_directional_distances(source, target, norm=norm)
    return backend.directional_nearest_neighbor_distances(source, target, norm=norm)


def _reduce_batch(values: ArrayLike, *, reduction: str) -> ArrayLike:
    return values if reduction == "none" else backend.mean_over_batch(values)


def chamfer_distance(
    source: MetricInput,
    target: MetricInput,
    *,
    norm: str = "l2",
    bidirectional_reduction: str = "sum",
    reduction: str = "mean",
) -> ArrayLike:
    """计算点集之间的 Chamfer Distance。"""

    validate_norm(norm)
    validate_bidirectional_reduction(bidirectional_reduction)
    validate_reduction(reduction)

    source_points = backend.to_coordinate_array(unwrap_metric_input(source, name="source"))
    target_points = backend.to_coordinate_array(unwrap_metric_input(target, name="target"))
    ensure_same_backend(
        source_points,
        target_points,
        first_name="source",
        second_name="target",
    )
    validate_matching_batch_shape(source_points, target_points)

    forward_distances = _directional_nearest_neighbor_distances(
        source_points,
        target_points,
        norm=norm,
    )
    backward_distances = _directional_nearest_neighbor_distances(
        target_points,
        source_points,
        norm=norm,
    )

    forward_scores = backend.mean_over_points(forward_distances)
    backward_scores = backend.mean_over_points(backward_distances)
    scores = forward_scores + backward_scores
    if bidirectional_reduction == "mean":
        scores = scores / 2
    return _reduce_batch(scores, reduction=reduction)


def hausdorff_distance(
    source: MetricInput,
    target: MetricInput,
    *,
    norm: str = "l2",
    directed: bool = False,
    reduction: str = "mean",
) -> ArrayLike:
    """计算点集之间的 Hausdorff Distance。"""

    validate_norm(norm)
    validate_reduction(reduction)

    source_points = backend.to_coordinate_array(unwrap_metric_input(source, name="source"))
    target_points = backend.to_coordinate_array(unwrap_metric_input(target, name="target"))
    ensure_same_backend(
        source_points,
        target_points,
        first_name="source",
        second_name="target",
    )
    validate_matching_batch_shape(source_points, target_points)

    forward_distances = _directional_nearest_neighbor_distances(
        source_points,
        target_points,
        norm=norm,
    )
    forward_scores = backend.max_over_points(forward_distances)

    if directed:
        return _reduce_batch(forward_scores, reduction=reduction)

    backward_distances = _directional_nearest_neighbor_distances(
        target_points,
        source_points,
        norm=norm,
    )
    backward_scores = backend.max_over_points(backward_distances)
    return _reduce_batch(
        backend.maximum(forward_scores, backward_scores),
        reduction=reduction,
    )
