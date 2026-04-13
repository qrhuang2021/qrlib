import pytest

import qrlib.metrics.distance as distance_module
from qrlib.metrics import chamfer_distance, hausdorff_distance

torch = pytest.importorskip("torch")


def test_torch_metrics_return_tensors() -> None:
    source = torch.tensor([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]], dtype=torch.float32)
    target = torch.tensor([[0.0, 0.0, 0.0]], dtype=torch.float32)

    cd_score = chamfer_distance(source, target, reduction="none")
    hd_score = hausdorff_distance(source, target, directed=True, reduction="none")

    assert isinstance(cd_score, torch.Tensor)
    assert isinstance(hd_score, torch.Tensor)
    assert torch.allclose(cd_score, torch.tensor(1.0, dtype=torch.float32))
    assert torch.allclose(hd_score, torch.tensor(2.0, dtype=torch.float32))


def test_torch_metrics_support_batched_reduction_modes() -> None:
    source = torch.tensor(
        [
            [[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]],
            [[0.0, 0.0, 0.0], [3.0, 0.0, 0.0]],
        ],
        dtype=torch.float32,
    )
    target = torch.tensor(
        [
            [[0.0, 0.0, 0.0]],
            [[0.0, 0.0, 0.0]],
        ],
        dtype=torch.float32,
    )

    batch_scores = chamfer_distance(source, target, reduction="none")
    mean_score = chamfer_distance(source, target, reduction="mean")

    assert torch.allclose(batch_scores, torch.tensor([1.0, 1.5], dtype=torch.float32))
    assert torch.allclose(mean_score, torch.tensor(1.25, dtype=torch.float32))


def test_torch_input_never_uses_scipy_path(monkeypatch: pytest.MonkeyPatch) -> None:
    source = torch.tensor([[0.0, 0.0, 0.0]], dtype=torch.float32)
    target = torch.tensor([[1.0, 0.0, 0.0]], dtype=torch.float32)

    def unexpected_scipy_call(*args: object, **kwargs: object) -> torch.Tensor:
        raise AssertionError("torch 输入不应走 SciPy 快路径")

    monkeypatch.setattr(distance_module, "SCIPY_AVAILABLE", True)
    monkeypatch.setattr(distance_module, "scipy_directional_distances", unexpected_scipy_call)

    score = hausdorff_distance(source, target, reduction="none")

    assert torch.allclose(score, torch.tensor(1.0, dtype=torch.float32))
