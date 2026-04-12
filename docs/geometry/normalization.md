# qrlib.geometry.normalization

`qrlib.geometry.normalization` 统一实现点云、网格和原始坐标数组的归一化与反归一化逻辑，并屏蔽 `numpy` / `torch` 的后端差异。

## 对外接口

### `normalize_to_sphere(data, center=(0, 0, 0), radius=1.0, eps=1e-8)`

- 自动计算输入数据的源中心与源尺度
- 把几何映射到目标球内
- 返回 `(normalized_data, source_center, source_scale)`

这里的 `source_center` 是点坐标均值，`source_scale` 是所有点到该中心的最大欧氏距离。

### `normalize_to_cube(data, center=(0, 0, 0), edge_length=2.0, eps=1e-8)`

- 自动计算包围盒中心与尺度
- 把几何映射到目标立方体内
- 返回 `(normalized_data, source_center, source_scale)`

这里的 `source_center` 是包围盒中心，`source_scale` 是半边长对应的最大轴向尺度。

### `normalize(data, center, scale, eps=1e-8)`

- 使用显式 `center` 和 `scale` 做归一化
- 返回与输入同类型的数据

### `denormalize(data, center, scale, eps=1e-8)`

- 使用显式 `center` 和 `scale` 把数据还原回原坐标系
- 返回与输入同类型的数据

## 返回值约定

- 输入 `numpy.ndarray`，输出 `numpy.ndarray`
- 输入 `torch.Tensor`，输出 `torch.Tensor`
- 输入 `PointCloud`，输出 `PointCloud`
- 输入 `Mesh`，输出 `Mesh`
- 对网格做变换时，只修改顶点，不修改面索引

## 示例：归一化到目标立方体并还原

```python
import numpy as np

from qrlib.geometry import denormalize, normalize, normalize_to_cube

points = np.array(
    [
        [0.0, 0.0, 0.0],
        [2.0, 2.0, 2.0],
    ],
    dtype=np.float32,
)

normalized_points, source_center, source_scale = normalize_to_cube(
    points,
    center=(5.0, 5.0, 5.0),
    edge_length=4.0,
)

unit_points = normalize(normalized_points, center=(5.0, 5.0, 5.0), scale=2.0)
restored_points = denormalize(unit_points, center=source_center, scale=source_scale)
```

## 常见边界

- `radius`、`edge_length`、`scale` 必须大于等于最小阈值，否则会抛出 `ValueError`
- `center` 必须能广播到坐标 shape 的批次维度
- `scale` 必须是标量，或可广播到输入坐标的批次维度

## 适合优先使用哪一个

- 想得到球内约束时，用 `normalize_to_sphere`
- 想得到轴对齐立方体约束时，用 `normalize_to_cube`
- 已经有明确中心和尺度时，用 `normalize`
- 需要恢复到原始坐标系时，用 `denormalize`

完整示例见 `examples/geometry_workflow.py`。
