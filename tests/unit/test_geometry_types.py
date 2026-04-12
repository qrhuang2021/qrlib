import numpy as np
import pytest

from qrlib.geometry import Mesh, PointCloud


def test_point_cloud_rejects_invalid_point_shape() -> None:
    with pytest.raises(ValueError, match="shape"):
        PointCloud(np.array([0.0, 1.0, 2.0], dtype=np.float32))


def test_mesh_rejects_non_integer_faces() -> None:
    with pytest.raises(ValueError, match="integer dtype"):
        Mesh(
            vertices=np.array(
                [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
                dtype=np.float32,
            ),
            faces=np.array([[0.0, 1.0, 2.0]], dtype=np.float32),
        )


def test_mesh_rejects_backend_mismatch() -> None:
    torch = pytest.importorskip("torch")

    with pytest.raises(TypeError, match="same backend family"):
        Mesh(
            vertices=np.array(
                [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
                dtype=np.float32,
            ),
            faces=torch.tensor([[0, 1, 2]], dtype=torch.int64),
        )
