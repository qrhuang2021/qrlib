# qrlib.geometry

`qrlib.geometry` 提供面向三维几何数据的稳定公开接口，当前聚焦两类能力：

- 基础几何类型：`PointCloud`、`Mesh`
- 几何归一化：`normalize_to_sphere`、`normalize_to_cube`、`normalize`、`denormalize`

## 推荐导入方式

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

### `PointCloud(points)`

- `points` 必须是 `numpy.ndarray` 或 `torch.Tensor`
- shape 必须为 `(N, 3)` 或 `(..., N, 3)`
- 输出会保持与输入同一后端族

### `Mesh(vertices, faces)`

- `vertices` 必须是 `numpy.ndarray` 或 `torch.Tensor`
- `vertices` 的 shape 必须为 `(N, 3)` 或 `(..., N, 3)`
- `faces` 必须是二维整数矩阵，shape 为 `(F, K)` 且 `K >= 3`
- `vertices` 与 `faces` 必须使用同一后端族

## 函数签名

```python
def normalize_to_sphere(data, center=(0.0, 0.0, 0.0), radius=1.0, eps=1e-8)
def normalize_to_cube(data, center=(0.0, 0.0, 0.0), edge_length=2.0, eps=1e-8)
def normalize(data, center, scale, eps=1e-8)
def denormalize(data, center, scale, eps=1e-8)
```

## 返回值约定

- 输入 `numpy.ndarray`，输出 `numpy.ndarray`
- 输入 `torch.Tensor`，输出 `torch.Tensor`
- 输入 `PointCloud`，输出 `PointCloud`
- 输入 `Mesh`，输出 `Mesh`
- 对 `Mesh` 做变换时，只修改顶点，不修改面索引

## 归一化语义

### `normalize_to_sphere`

- 使用点坐标均值作为源中心
- 使用最大欧氏距离作为源尺度
- 返回 `(normalized_data, source_center, source_scale)`

### `normalize_to_cube`

- 使用包围盒中心作为源中心
- 使用最大半边长作为源尺度
- 返回 `(normalized_data, source_center, source_scale)`

### `normalize` / `denormalize`

- 接收显式 `center` 与 `scale`
- 适用于需要在统一空间与原始空间之间往返变换的流程

## 错误语义

以下情况会抛出 `ValueError` 或 `TypeError`：

- 点坐标形状非法
- 面索引不是二维整数数组
- `numpy` 与 `torch` 后端混用
- `radius`、`edge_length` 或 `scale` 小于最小阈值
- `center` 或 `scale` 无法广播到输入批次维度
