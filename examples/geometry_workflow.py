"""演示 qrlib.geometry 的基础类型、归一化与反归一化流程。"""

import numpy as np

from qrlib.geometry import (
    Mesh,
    PointCloud,
    denormalize,
    normalize,
    normalize_to_cube,
    normalize_to_sphere,
)


def main() -> None:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [2.0, 2.0, 2.0],
            [1.0, 0.0, 1.0],
        ],
        dtype=np.float32,
    )
    cloud = PointCloud(points)

    mesh = Mesh(
        vertices=np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ],
            dtype=np.float32,
        ),
        faces=np.array(
            [
                [0, 1, 2],
                [0, 1, 3],
            ],
            dtype=np.int64,
        ),
    )

    normalized_cloud, sphere_center, sphere_scale = normalize_to_sphere(cloud, radius=1.5)
    normalized_points, cube_center, cube_scale = normalize_to_cube(
        points,
        center=(5.0, 5.0, 5.0),
        edge_length=4.0,
    )
    unit_points = normalize(normalized_points, center=(5.0, 5.0, 5.0), scale=2.0)
    restored_points = denormalize(unit_points, center=cube_center, scale=cube_scale)
    normalized_mesh = mesh.normalize(center=(0.5, 0.5, 0.5), scale=0.5)

    print("PointCloud 点数:", cloud.points.shape[-2])
    print("Mesh 顶点数:", mesh.vertices.shape[-2])
    print("Mesh 面数:", mesh.faces.shape[-2])
    print("球归一化后的点云:")
    print(normalized_cloud.points)
    print("球归一化源中心:", sphere_center)
    print("球归一化源尺度:", sphere_scale)
    print("立方体归一化结果:")
    print(normalized_points)
    print("立方体归一化源中心:", cube_center)
    print("立方体归一化源尺度:", cube_scale)
    print("还原后是否与原始点一致:", np.allclose(restored_points, points))
    print("网格归一化后是否保留面索引:", np.array_equal(normalized_mesh.faces, mesh.faces))


if __name__ == "__main__":
    main()
