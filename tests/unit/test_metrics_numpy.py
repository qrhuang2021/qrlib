import numpy as np
import pytest

import qrlib.metrics.distance as distance_module
from qrlib.metrics import chamfer_distance, hausdorff_distance
from qrlib.metrics._backend import backend
from qrlib.metrics._scipy import SCIPY_AVAILABLE, directional_nearest_neighbor_distances


def test_chamfer_distance_supports_l1_and_l2() -> None:
    source = np.array([[1.0, 1.0, 0.0]], dtype=np.float32)
    target = np.array([[0.0, 0.0, 0.0]], dtype=np.float32)

    l1_score = chamfer_distance(source, target, norm="l1", reduction="none")
    l2_score = chamfer_distance(source, target, norm="l2", reduction="none")

    np.testing.assert_allclose(np.asarray(l1_score), np.array(4.0, dtype=np.float32))
    np.testing.assert_allclose(
        np.asarray(l2_score),
        np.array(2 * np.sqrt(2), dtype=np.float32),
        rtol=1e-6,
    )


def test_chamfer_distance_supports_bidirectional_mean() -> None:
    source = np.array([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]], dtype=np.float32)
    target = np.array([[0.0, 0.0, 0.0]], dtype=np.float32)

    sum_score = chamfer_distance(
        source,
        target,
        bidirectional_reduction="sum",
        reduction="none",
    )
    mean_score = chamfer_distance(
        source,
        target,
        bidirectional_reduction="mean",
        reduction="none",
    )

    np.testing.assert_allclose(np.asarray(sum_score), np.array(1.0, dtype=np.float32))
    np.testing.assert_allclose(np.asarray(mean_score), np.array(0.5, dtype=np.float32))


def test_chamfer_distance_supports_batched_reduction_modes() -> None:
    source = np.array(
        [
            [[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]],
            [[0.0, 0.0, 0.0], [3.0, 0.0, 0.0]],
        ],
        dtype=np.float32,
    )
    target = np.array(
        [
            [[0.0, 0.0, 0.0]],
            [[0.0, 0.0, 0.0]],
        ],
        dtype=np.float32,
    )

    batch_scores = chamfer_distance(source, target, reduction="none")
    mean_score = chamfer_distance(source, target, reduction="mean")

    np.testing.assert_allclose(batch_scores, np.array([1.0, 1.5], dtype=np.float32))
    np.testing.assert_allclose(np.asarray(mean_score), np.array(1.25, dtype=np.float32))


def test_hausdorff_distance_supports_directed_and_symmetric() -> None:
    source = np.array([[0.0, 0.0, 0.0]], dtype=np.float32)
    target = np.array([[2.0, 0.0, 0.0], [3.0, 0.0, 0.0]], dtype=np.float32)

    directed_score = hausdorff_distance(source, target, directed=True, reduction="none")
    symmetric_score = hausdorff_distance(source, target, directed=False, reduction="none")

    np.testing.assert_allclose(np.asarray(directed_score), np.array(2.0, dtype=np.float32))
    np.testing.assert_allclose(np.asarray(symmetric_score), np.array(3.0, dtype=np.float32))


@pytest.mark.skipif(not SCIPY_AVAILABLE, reason="SciPy 不可用时跳过快路径一致性测试")
def test_scipy_directional_distances_match_dense_backend() -> None:
    source = np.array(
        [
            [[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]],
            [[1.0, 1.0, 0.0], [2.0, 2.0, 0.0]],
        ],
        dtype=np.float32,
    )
    target = np.array(
        [
            [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
            [[0.0, 0.0, 0.0], [3.0, 3.0, 0.0]],
        ],
        dtype=np.float32,
    )

    scipy_distances = directional_nearest_neighbor_distances(source, target, norm="l2")
    dense_distances = backend.directional_nearest_neighbor_distances(source, target, norm="l2")

    np.testing.assert_allclose(scipy_distances, dense_distances, rtol=1e-6)


def test_numpy_input_prefers_scipy_path_when_available(monkeypatch: pytest.MonkeyPatch) -> None:
    source = np.array([[0.0, 0.0, 0.0]], dtype=np.float32)
    target = np.array([[1.0, 0.0, 0.0]], dtype=np.float32)
    calls: list[str] = []

    def fake_scipy_distances(
        source_points: np.ndarray, target_points: np.ndarray, *, norm: str
    ) -> np.ndarray:
        calls.append(norm)
        return backend.directional_nearest_neighbor_distances(
            source_points, target_points, norm=norm
        )

    monkeypatch.setattr(distance_module, "SCIPY_AVAILABLE", True)
    monkeypatch.setattr(distance_module, "scipy_directional_distances", fake_scipy_distances)

    score = chamfer_distance(source, target, reduction="none")

    np.testing.assert_allclose(np.asarray(score), np.array(2.0, dtype=np.float32))
    assert calls == ["l2", "l2"]


def test_numpy_input_can_fall_back_when_scipy_is_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    source = np.array([[0.0, 0.0, 0.0]], dtype=np.float32)
    target = np.array([[1.0, 0.0, 0.0]], dtype=np.float32)

    def unexpected_scipy_call(*args: object, **kwargs: object) -> np.ndarray:
        raise AssertionError("SciPy 快路径不应在禁用后被调用")

    monkeypatch.setattr(distance_module, "SCIPY_AVAILABLE", False)
    monkeypatch.setattr(distance_module, "scipy_directional_distances", unexpected_scipy_call)

    score = chamfer_distance(source, target, reduction="none")

    np.testing.assert_allclose(np.asarray(score), np.array(2.0, dtype=np.float32))
