# qrlib.geometry

`qrlib.geometry` 提供面向三维几何数据的稳定公共接口，当前聚焦两类能力：

- 基础几何类型：`PointCloud`、`Mesh`
- 几何归一化：`normalize_to_sphere`、`normalize_to_cube`、`normalize`、`denormalize`

这个子包同时支持 `numpy.ndarray` 与可选的 `torch.Tensor`。输入是数组时，输出仍然保持数组；输入是 `PointCloud` 或 `Mesh` 时，输出会重建为同类型对象。

## 对外接口

```python
from qrlib.geometry import (
    Mesh,
    PointCloud,
    denormalize,
    normalize,
    normalize_to_cube,
    normalize_to_sphere,
)
```

## 基础类型

### `PointCloud`

`PointCloud(points)` 用于表示点云坐标。

约束如下：

- `points` 必须是 `numpy.ndarray` 或 `torch.Tensor`
- shape 必须为 `(N, 3)` 或 `(..., N, 3)`
- 坐标最后一维固定为 3

### `Mesh`

`Mesh(vertices, faces)` 用于表示网格顶点与面索引。

约束如下：

- `vertices` 必须是 `numpy.ndarray` 或 `torch.Tensor`
- `vertices` 的 shape 必须为 `(N, 3)` 或 `(..., N, 3)`
- `faces` 必须是二维整数矩阵，shape 为 `(F, K)`，且 `K >= 3`
- `vertices` 与 `faces` 必须使用同一后端族，不能混用 `numpy` 和 `torch`

## 设计约定

- `PointCloud` 与 `Mesh` 负责承载几何数据与输入校验
- 归一化逻辑统一复用模块级接口
- 输入是数组时返回数组，输入是 `PointCloud` 或 `Mesh` 时返回同类型对象
- 对网格做几何变换时，只修改顶点，不修改面索引

## 适用场景

- 训练前把点云映射到统一球或统一立方体
- 需要保留网格面索引，只变换顶点坐标
- 在归一化空间和原始坐标空间之间往返变换
- 统一处理 `numpy` 与 `torch` 的几何输入

## 快速示例

```python
import numpy as np

from qrlib.geometry import PointCloud, normalize_to_sphere

points = np.array(
    [
        [0.0, 0.0, 0.0],
        [2.0, 0.0, 0.0],
        [1.0, 1.0, 0.0],
    ],
    dtype=np.float32,
)
cloud = PointCloud(points)

normalized_cloud, source_center, source_scale = normalize_to_sphere(cloud)

print(normalized_cloud.points)
print(source_center)
print(source_scale)
```

## 进一步阅读

- [归一化接口说明](normalization.md)

## 对应示例

- `examples/geometry_workflow.py`
