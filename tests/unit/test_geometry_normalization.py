import numpy as np
import pytest

from qrlib.geometry import (
    Mesh,
    PointCloud,
    denormalize,
    normalize,
    normalize_to_cube,
    normalize_to_sphere,
)


def test_normalize_to_sphere_places_points_inside_unit_sphere() -> None:
    points = np.array([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0], [1.0, 1.0, 0.0]], dtype=np.float32)

    normalized_points, source_center, source_scale = normalize_to_sphere(points)

    assert isinstance(normalized_points, np.ndarray)
    np.testing.assert_allclose(source_center, np.array([1.0, 1.0 / 3.0, 0.0], dtype=np.float32))
    np.testing.assert_allclose(
        source_scale,
        np.linalg.norm(points - source_center, axis=-1).max(),
    )
    assert np.all(np.linalg.norm(normalized_points, axis=-1) <= 1.0 + 1e-6)


def test_normalize_to_sphere_supports_custom_target() -> None:
    points = np.array([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]], dtype=np.float32)

    normalized_points, source_center, source_scale = normalize_to_sphere(
        points,
        center=(1.0, 2.0, 3.0),
        radius=2.0,
    )

    np.testing.assert_allclose(
        normalized_points,
        np.array([[-1.0, 2.0, 3.0], [3.0, 2.0, 3.0]], dtype=np.float32),
    )
    np.testing.assert_allclose(source_center, np.array([1.0, 0.0, 0.0], dtype=np.float32))
    np.testing.assert_allclose(source_scale, np.array(1.0, dtype=np.float32))


def test_normalize_to_sphere_supports_batched_points() -> None:
    points = np.array(
        [
            [[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]],
            [[0.0, 0.0, 0.0], [0.0, 4.0, 0.0]],
        ],
        dtype=np.float32,
    )

    normalized_points, source_center, source_scale = normalize_to_sphere(points)

    np.testing.assert_allclose(
        source_center,
        np.array([[1.0, 0.0, 0.0], [0.0, 2.0, 0.0]], dtype=np.float32),
    )
    np.testing.assert_allclose(source_scale, np.array([1.0, 2.0], dtype=np.float32))
    np.testing.assert_allclose(
        normalized_points,
        np.array(
            [
                [[-1.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
                [[0.0, -1.0, 0.0], [0.0, 1.0, 0.0]],
            ],
            dtype=np.float32,
        ),
    )
    assert np.all(np.linalg.norm(normalized_points, axis=-1) <= 1.0 + 1e-6)


def test_normalize_to_cube_places_points_inside_unit_cube() -> None:
    points = np.array([[0.0, 0.0, 0.0], [2.0, 4.0, 6.0]], dtype=np.float32)

    normalized_points, source_center, source_scale = normalize_to_cube(points)

    assert isinstance(normalized_points, np.ndarray)
    np.testing.assert_allclose(source_center, np.array([1.0, 2.0, 3.0], dtype=np.float32))
    np.testing.assert_allclose(source_scale, np.array(3.0, dtype=np.float32))
    assert np.all(normalized_points <= 1.0 + 1e-6)
    assert np.all(normalized_points >= -1.0 - 1e-6)


def test_normalize_to_cube_supports_custom_target() -> None:
    points = np.array([[0.0, 0.0, 0.0], [2.0, 2.0, 2.0]], dtype=np.float32)

    normalized_points, source_center, source_scale = normalize_to_cube(
        points,
        center=(5.0, 5.0, 5.0),
        edge_length=4.0,
    )

    np.testing.assert_allclose(
        normalized_points,
        np.array([[3.0, 3.0, 3.0], [7.0, 7.0, 7.0]], dtype=np.float32),
    )
    np.testing.assert_allclose(source_center, np.array([1.0, 1.0, 1.0], dtype=np.float32))
    np.testing.assert_allclose(source_scale, np.array(1.0, dtype=np.float32))


def test_normalize_and_denormalize_round_trip_array() -> None:
    points = np.array([[1.0, 2.0, 3.0], [5.0, 6.0, 7.0]], dtype=np.float32)

    normalized_points = normalize(points, center=(1.0, 2.0, 3.0), scale=2.0)
    restored_points = denormalize(normalized_points, center=(1.0, 2.0, 3.0), scale=2.0)

    np.testing.assert_allclose(restored_points, points)


def test_normalize_and_denormalize_round_trip_batched_array() -> None:
    points = np.array(
        [
            [[1.0, 2.0, 3.0], [5.0, 6.0, 7.0]],
            [[2.0, 4.0, 6.0], [8.0, 10.0, 12.0]],
        ],
        dtype=np.float32,
    )
    center = np.array([[1.0, 2.0, 3.0], [2.0, 4.0, 6.0]], dtype=np.float32)
    scale = np.array([2.0, 3.0], dtype=np.float32)

    normalized_points = normalize(points, center=center, scale=scale)
    restored_points = denormalize(normalized_points, center=center, scale=scale)

    np.testing.assert_allclose(
        normalized_points,
        np.array(
            [
                [[0.0, 0.0, 0.0], [2.0, 2.0, 2.0]],
                [[0.0, 0.0, 0.0], [2.0, 2.0, 2.0]],
            ],
            dtype=np.float32,
        ),
    )
    np.testing.assert_allclose(restored_points, points)


def test_point_cloud_methods_share_module_logic() -> None:
    points = np.array([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]], dtype=np.float32)
    cloud = PointCloud(points)

    normalized_cloud, source_center, source_scale = cloud.normalize_to_sphere()
    normalized_points, expected_center, expected_scale = normalize_to_sphere(points)

    assert isinstance(normalized_cloud, PointCloud)
    np.testing.assert_allclose(normalized_cloud.points, normalized_points)
    np.testing.assert_allclose(source_center, expected_center)
    np.testing.assert_allclose(source_scale, expected_scale)


def test_mesh_round_trip_keeps_faces() -> None:
    mesh = Mesh(
        vertices=np.array(
            [[0.0, 0.0, 0.0], [2.0, 0.0, 0.0], [0.0, 2.0, 0.0]],
            dtype=np.float32,
        ),
        faces=np.array([[0, 1, 2]], dtype=np.int64),
    )

    normalized_mesh = normalize(mesh, center=(1.0, 1.0, 0.0), scale=2.0)
    restored_mesh = denormalize(normalized_mesh, center=(1.0, 1.0, 0.0), scale=2.0)

    assert isinstance(normalized_mesh, Mesh)
    np.testing.assert_array_equal(normalized_mesh.faces, mesh.faces)
    np.testing.assert_allclose(restored_mesh.vertices, mesh.vertices)
    np.testing.assert_array_equal(restored_mesh.faces, mesh.faces)


def test_custom_target_can_round_trip_back_to_source_space() -> None:
    points = np.array([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]], dtype=np.float32)

    normalized_points, source_center, source_scale = normalize_to_sphere(
        points,
        center=(10.0, 20.0, 30.0),
        radius=3.0,
    )
    unit_points = normalize(normalized_points, center=(10.0, 20.0, 30.0), scale=3.0)
    restored_points = denormalize(unit_points, center=source_center, scale=source_scale)

    np.testing.assert_allclose(restored_points, points)


def test_normalize_rejects_invalid_scale() -> None:
    points = np.array([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]], dtype=np.float32)

    with pytest.raises(ValueError, match="scale"):
        normalize(points, center=(0.0, 0.0, 0.0), scale=0.0)


def test_normalize_to_sphere_rejects_invalid_radius() -> None:
    points = np.array([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]], dtype=np.float32)

    with pytest.raises(ValueError, match="radius"):
        normalize_to_sphere(points, radius=0.0)


def test_normalize_to_cube_rejects_invalid_edge_length() -> None:
    points = np.array([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]], dtype=np.float32)

    with pytest.raises(ValueError, match="edge_length"):
        normalize_to_cube(points, edge_length=0.0)
