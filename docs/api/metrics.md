# qrlib.metrics

`qrlib.metrics` 提供面向点集的稳定距离指标接口，当前包含：

- `chamfer_distance`
- `hausdorff_distance`

## 推荐导入方式

```python
from qrlib.metrics import chamfer_distance, hausdorff_distance
```

## 输入约定

- `source` 与 `target` 接受：
  - `numpy.ndarray`
  - `torch.Tensor`
  - `qrlib.geometry.PointCloud`
- 解包后的点坐标 shape 必须为 `(N, 3)` 或 `(..., N, 3)`
- 两侧点数可以不同
- 两侧 batch 前缀必须完全一致
- 点集不能为空
- `numpy` 与 `torch` 后端不能混用

## 函数签名

```python
def chamfer_distance(
    source,
    target,
    *,
    norm="l2",
    bidirectional_reduction="sum",
    reduction="mean",
)

def hausdorff_distance(
    source,
    target,
    *,
    norm="l2",
    directed=False,
    reduction="mean",
)
```

## 返回值约定

- `reduction="none"`：返回逐 batch 结果
- `reduction="mean"`：返回 batch 均值
- `numpy` 输入返回 `numpy` 标量或数组
- `torch` 输入返回 `torch` 标量或张量

## 指标语义

### `chamfer_distance`

- 每个方向先计算最近邻距离
- 再按点维做均值
- 最后按 `bidirectional_reduction` 聚合双向结果：
  - `"sum"`：前向与后向直接相加
  - `"mean"`：前向与后向求平均

### `hausdorff_distance`

- `directed=True`：返回 `source -> target`
- `directed=False`：返回双向最大值

## 范数与加速

- `norm="l1"`：曼哈顿距离
- `norm="l2"`：欧氏距离
- 基础功能不依赖 SciPy
- 若安装 `qrlib[scipy]`，`numpy` 输入会自动使用 `scipy.spatial.KDTree` 快路径
- `torch` 输入始终走纯 `torch` 路径

## 错误语义

以下情况会抛出 `ValueError` 或 `TypeError`：

- 非法输入类型
- 点坐标 shape 非法
- 点集为空
- `numpy` 与 `torch` 后端混用
- batch 前缀不一致
- 非法 `norm`
- 非法 `reduction`
- 非法 `bidirectional_reduction`
