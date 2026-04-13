import numpy as np
import pytest

import qrlib.metrics as metrics
from qrlib.geometry import PointCloud
from qrlib.metrics import chamfer_distance, hausdorff_distance


def test_metrics_module_exports_public_api() -> None:
    assert metrics.__all__ == ["chamfer_distance", "hausdorff_distance"]


def test_point_cloud_input_matches_array_input() -> None:
    source_points = np.array([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]], dtype=np.float32)
    target_points = np.array([[0.0, 0.0, 0.0]], dtype=np.float32)

    cloud_score = chamfer_distance(
        PointCloud(source_points),
        PointCloud(target_points),
        reduction="none",
    )
    array_score = chamfer_distance(source_points, target_points, reduction="none")

    np.testing.assert_allclose(np.asarray(cloud_score), np.asarray(array_score))


def test_chamfer_distance_rejects_invalid_norm() -> None:
    points = np.array([[0.0, 0.0, 0.0]], dtype=np.float32)

    with pytest.raises(ValueError, match="norm"):
        chamfer_distance(points, points, norm="l3")


def test_hausdorff_distance_rejects_invalid_reduction() -> None:
    points = np.array([[0.0, 0.0, 0.0]], dtype=np.float32)

    with pytest.raises(ValueError, match="reduction"):
        hausdorff_distance(points, points, reduction="sum")


def test_chamfer_distance_rejects_invalid_bidirectional_reduction() -> None:
    points = np.array([[0.0, 0.0, 0.0]], dtype=np.float32)

    with pytest.raises(ValueError, match="bidirectional_reduction"):
        chamfer_distance(points, points, bidirectional_reduction="max")


def test_metrics_reject_empty_point_sets() -> None:
    empty_points = np.empty((0, 3), dtype=np.float32)
    points = np.array([[0.0, 0.0, 0.0]], dtype=np.float32)

    with pytest.raises(ValueError, match="at least one point"):
        chamfer_distance(empty_points, points)


def test_metrics_reject_invalid_point_shape() -> None:
    invalid_points = np.array([0.0, 1.0, 2.0], dtype=np.float32)
    points = np.array([[0.0, 0.0, 0.0]], dtype=np.float32)

    with pytest.raises(ValueError, match="shape"):
        hausdorff_distance(invalid_points, points)


def test_metrics_reject_batch_shape_mismatch() -> None:
    source = np.zeros((2, 1, 3), dtype=np.float32)
    target = np.zeros((3, 1, 3), dtype=np.float32)

    with pytest.raises(ValueError, match="same batch shape|share the same batch shape"):
        chamfer_distance(source, target)


def test_metrics_reject_backend_mismatch() -> None:
    torch = pytest.importorskip("torch")
    source = np.zeros((1, 3), dtype=np.float32)
    target = torch.zeros((1, 3), dtype=torch.float32)

    with pytest.raises(TypeError, match="same backend family"):
        chamfer_distance(source, target)
