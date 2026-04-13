# 几何归一化工作流

这个教程展示 `qrlib.geometry` 的一个完整使用路径：

1. 创建点云与网格对象
2. 把点云映射到目标球内
3. 把数组映射到目标立方体内
4. 在归一化空间与原始坐标空间之间往返
5. 保持网格面索引不变，只变换顶点

## 1. 构造输入

```python
import numpy as np

from qrlib.geometry import Mesh, PointCloud

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
```

## 2. 归一化到目标球

```python
from qrlib.geometry import normalize_to_sphere

normalized_cloud, source_center, source_scale = normalize_to_sphere(cloud, radius=1.5)
```

这一步会返回三部分：

- 归一化后的数据
- 源中心
- 源尺度

如果输入是 `PointCloud`，输出仍然是 `PointCloud`。

## 3. 归一化到目标立方体

```python
from qrlib.geometry import normalize_to_cube

normalized_points, cube_center, cube_scale = normalize_to_cube(
    points,
    center=(5.0, 5.0, 5.0),
    edge_length=4.0,
)
```

这一步会把点坐标映射到边长为 4、中心为 `(5, 5, 5)` 的立方体内。

## 4. 从目标空间回到原始坐标空间

```python
from qrlib.geometry import denormalize, normalize

unit_points = normalize(normalized_points, center=(5.0, 5.0, 5.0), scale=2.0)
restored_points = denormalize(unit_points, center=cube_center, scale=cube_scale)
```

适合在“先映射到统一空间做处理，再恢复原坐标”的场景中使用。

## 5. 只变换网格顶点，不改面索引

```python
normalized_mesh = mesh.normalize(center=(0.5, 0.5, 0.5), scale=0.5)
```

`qrlib.geometry` 对 `Mesh` 做归一化时，只会修改 `vertices`，不会改写 `faces`。

## 相关入口

- [qrlib.geometry API](../api/geometry.md)
- [仓库架构](../concepts/architecture.md)
