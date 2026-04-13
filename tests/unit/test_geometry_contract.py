import numpy as np
import pytest

from qrlib.geometry import Mesh, PointCloud, normalize
from qrlib.geometry.types import Mesh as MeshFromTypes
from qrlib.geometry.types import PointCloud as PointCloudFromTypes


def test_types_module_keeps_public_reexports() -> None:
    assert PointCloudFromTypes is PointCloud
    assert MeshFromTypes is Mesh


def test_normalize_rejects_non_broadcastable_center() -> None:
    points = np.array([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]], dtype=np.float32)

    with pytest.raises(ValueError, match="center"):
        normalize(points, center=np.array([0.0, 0.0], dtype=np.float32), scale=1.0)


def test_normalize_rejects_non_broadcastable_scale() -> None:
    points = np.array([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]], dtype=np.float32)

    with pytest.raises(ValueError, match="scale"):
        normalize(
            points,
            center=(0.0, 0.0, 0.0),
            scale=np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32),
        )
