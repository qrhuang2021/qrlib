import pytest

from qrlib.geometry import Mesh, denormalize, normalize, normalize_to_sphere

torch = pytest.importorskip("torch")


def test_torch_points_round_trip() -> None:
    points = torch.tensor([[1.0, 2.0, 3.0], [5.0, 6.0, 7.0]], dtype=torch.float32)

    normalized_points = normalize(points, center=(1.0, 2.0, 3.0), scale=2.0)
    restored_points = denormalize(normalized_points, center=(1.0, 2.0, 3.0), scale=2.0)

    assert isinstance(normalized_points, torch.Tensor)
    assert torch.allclose(restored_points, points)


def test_torch_mesh_normalize_to_sphere_keeps_faces() -> None:
    mesh = Mesh(
        vertices=torch.tensor(
            [[0.0, 0.0, 0.0], [2.0, 0.0, 0.0], [0.0, 2.0, 0.0]],
            dtype=torch.float32,
        ),
        faces=torch.tensor([[0, 1, 2]], dtype=torch.int64),
    )

    normalized_mesh, source_center, source_scale = normalize_to_sphere(mesh)

    assert isinstance(normalized_mesh, Mesh)
    assert torch.equal(normalized_mesh.faces, mesh.faces)
    assert torch.allclose(source_center, torch.tensor([2.0 / 3.0, 2.0 / 3.0, 0.0]))
    assert torch.all(source_scale > 0)
