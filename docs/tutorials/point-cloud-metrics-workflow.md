# 点云距离指标工作流

这个教程展示 `qrlib.metrics` 的一个完整使用路径：

1. 准备源点集与目标点集
2. 使用 `PointCloud` 或裸数组计算 `CD`
3. 在 `L1` / `L2` 与双向聚合方式之间切换
4. 计算有向与对称 `HD`

## 1. 构造输入

```python
import numpy as np

from qrlib.geometry import PointCloud

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
```

## 2. 计算 Chamfer Distance

```python
from qrlib.metrics import chamfer_distance

cd_l2_sum = chamfer_distance(source_cloud, target_cloud)
cd_l1_mean = chamfer_distance(
    source_points,
    target_points,
    norm="l1",
    bidirectional_reduction="mean",
    reduction="none",
)
```

- 默认使用 `L2 + 双向求和 + batch 均值`
- 如果需要论文里常见的“加完以后除以 2”版本，可以把 `bidirectional_reduction` 设为 `"mean"`

## 3. 计算 Hausdorff Distance

```python
from qrlib.metrics import hausdorff_distance

hd_directed = hausdorff_distance(source_points, target_points, directed=True, reduction="none")
hd_symmetric = hausdorff_distance(source_points, target_points, reduction="none")
```

- `directed=True` 返回 `source -> target`
- 默认返回对称 Hausdorff

## 4. 可选启用 SciPy 快路径

基础功能不依赖 SciPy。

如果你希望在 `numpy` 的 CPU 路径上自动启用 `KDTree` 加速，可以安装：

```bash
pip install "qrlib[scipy]"
```

在仓库本地开发环境中，对应命令是：

```bash
uv pip install --python .venv/bin/python -e ".[dev,scipy]"
```

## 相关入口

- [qrlib.metrics API](../api/metrics.md)
- [快速开始](../getting-started.md)
- [仓库架构](../concepts/architecture.md)
