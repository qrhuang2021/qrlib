"""演示 qrlib.metrics 的点云距离指标工作流。"""

import numpy as np

from qrlib.geometry import PointCloud
from qrlib.metrics import chamfer_distance, hausdorff_distance


def main() -> None:
    source_points = np.array(
        [
            [0.0, 0.0, 0.0],
            [2.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
        ],
        dtype=np.float32,
    )
    target_points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
        ],
        dtype=np.float32,
    )

    source_cloud = PointCloud(source_points)
    target_cloud = PointCloud(target_points)

    cd_l2_sum = chamfer_distance(source_cloud, target_cloud)
    cd_l1_mean = chamfer_distance(
        source_points,
        target_points,
        norm="l1",
        bidirectional_reduction="mean",
        reduction="none",
    )
    hd_directed = hausdorff_distance(source_points, target_points, directed=True, reduction="none")
    hd_symmetric = hausdorff_distance(source_points, target_points, reduction="none")

    print("源点数:", source_points.shape[0])
    print("目标点数:", target_points.shape[0])
    print("CD (L2, 双向求和):", cd_l2_sum)
    print("CD (L1, 双向平均):", cd_l1_mean)
    print("HD (有向, source -> target):", hd_directed)
    print("HD (对称):", hd_symmetric)


if __name__ == "__main__":
    main()
