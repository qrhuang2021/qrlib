# 规范：点云距离指标

- `change slug`：`point-cloud-distance-metrics`
- 状态：`accepted`
- 负责人：qrlib maintainers

## 背景

`qrlib.metrics` 目前只保留了空的子包边界，还没有稳定公开的指标接口。
点云评估中的 Chamfer Distance（CD）与 Hausdorff Distance（HD）已经是多个项目都会反复复用的基础能力，适合沉淀为库级 API。

同时，这类指标既要兼顾 `numpy` / `torch` 双后端一致性，也要为纯 `numpy` 的 CPU 评估场景保留可选的 SciPy 加速路径。

## 目标

- 为点集提供稳定公开的 `chamfer_distance` 与 `hausdorff_distance` 接口
- 接受 `numpy.ndarray`、`torch.Tensor` 与 `PointCloud` 作为输入
- 支持 `(N, 3)` 与 `(..., N, 3)` 形状
- 支持 `L1` / `L2` 两种范数
- 支持 `CD` 的双向 `sum` / `mean` 组合方式
- 支持 `HD` 的有向与对称模式
- 在不引入强制运行时依赖的前提下，为 `numpy` 路径提供可选 SciPy 加速

## 非目标

- 不支持 `Mesh` 作为指标输入
- 不在 `PointCloud` 上新增实例方法
- 不实现近似最近邻、超大点云分块或半精度优化
- 不改变 `qrlib.__init__` 的顶层导出策略

## 公开契约

### 函数

- `chamfer_distance(source, target, *, norm="l2", bidirectional_reduction="sum", reduction="mean")`
- `hausdorff_distance(source, target, *, norm="l2", directed=False, reduction="mean")`

### 输入

- `source` 与 `target` 必须是 `numpy.ndarray`、`torch.Tensor` 或 `PointCloud`
- 解包后的点坐标 shape 必须为 `(N, 3)` 或 `(..., N, 3)`
- 两侧点数可以不同
- 两侧 batch 前缀必须完全一致，不做 batch broadcasting
- 点集不能为空
- `numpy` 与 `torch` 后端不能混用

### 返回值与语义

- 返回值保持输入后端族
- `reduction="none"` 返回逐 batch 结果
- `reduction="mean"` 返回 batch 均值
- `chamfer_distance`：
  - 每个方向先取最近邻距离
  - 再按点维做均值
  - 最后按 `bidirectional_reduction` 做双向 `sum` 或 `mean`
- `hausdorff_distance`：
  - `directed=True` 返回 `source -> target`
  - `directed=False` 返回 `max(source -> target, target -> source)`

### 错误语义

以下情况必须显式报错：

- 非法输入类型
- 非法点坐标 shape
- 空点集
- `numpy` / `torch` 后端混用
- batch 前缀不一致
- 非法 `norm`
- 非法 `reduction`
- 非法 `bidirectional_reduction`

### 依赖与加速

- 基础指标能力不依赖 SciPy
- 若安装 `qrlib[scipy]`，`numpy` 输入可自动使用 `scipy.spatial.KDTree` 作为快路径
- `torch` 输入始终使用纯 `torch` 路径，不引入 CPU 回退

## 验收标准

- `numpy` dense 路径的 `CD/HD` 数值测试通过
- `torch` 路径测试通过（若环境安装 torch）
- SciPy 可用时，`numpy` 快路径与 dense 路径结果一致
- SciPy 缺失时，`numpy` 路径仍可正常回退
- `PointCloud` 输入与裸数组输入结果一致
- 公开文档补齐 API 页、教程页、安装说明与导航入口
- 维护者规范、设计、代码、测试与公开文档保持一致
- `ruff check .`、`pytest`、`mkdocs build` 全部通过

## 迁移与兼容性

- 这是 `qrlib.metrics` 的首批稳定公开接口，不涉及破坏性迁移
- 顶层导入仍建议通过 `from qrlib.metrics import ...`
- SciPy 只作为可选依赖，不改变基础安装路径

## 开放问题

- 暂无
