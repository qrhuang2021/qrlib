# 设计：点云距离指标

- `change slug`：`point-cloud-distance-metrics`
- 对应规范：`../specs/point-cloud-distance-metrics.md`

## 总体方案

在 `qrlib.metrics` 内新增“公开 API + 输入校验 + dense 后端 + SciPy 快路径”四层结构，用统一公开函数提供 `CD/HD`，并在 `numpy` 输入时自动选择可用的最快实现。

## 模块拆分

- `src/qrlib/metrics/__init__.py`：稳定导出面
- `src/qrlib/metrics/distance.py`：公开 `chamfer_distance` / `hausdorff_distance`
- `src/qrlib/metrics/_typing.py`：内部类型别名与输入类型
- `src/qrlib/metrics/_validation.py`：输入解包、shape 校验、模式校验、后端校验
- `src/qrlib/metrics/_backend.py`：`numpy` / `torch` dense 最近邻与归约
- `src/qrlib/metrics/_scipy.py`：`numpy + scipy` 的 `KDTree` 快路径
- `tests/unit/test_metrics_contract.py`：接口与错误语义
- `tests/unit/test_metrics_numpy.py`：`numpy` dense / SciPy 结果
- `tests/unit/test_metrics_torch.py`：`torch` 路径
- `docs/api/metrics.md`：公开 API 文档
- `docs/tutorials/point-cloud-metrics-workflow.md`：公开教程

## 关键数据流

1. 公开函数接收 `numpy.ndarray`、`torch.Tensor` 或 `PointCloud`
2. `_validation.py` 负责解包 `PointCloud`、校验 shape / 空点集 / batch / 模式
3. `distance.py` 根据输入后端选择实现路径：
   - `torch` 输入：走 `_backend.py` 的 dense 路径
   - `numpy` 输入且 SciPy 可用：走 `_scipy.py` 的 `KDTree` 路径
   - `numpy` 输入且 SciPy 不可用：回退 `_backend.py` 的 dense 路径
4. 方向级最近邻结果返回后，在 `distance.py` 完成 `CD/HD` 的语义聚合与 `reduction`

## 备选方案与取舍

### 方案 A：只做 dense 实现

不采用。因为 `numpy` 的 CPU 评估场景下，3D 最近邻查询很适合 `KDTree`，完全放弃快路径会让大点云评估成本偏高。

### 方案 B：强依赖 SciPy

不采用。因为这会改变基础运行时依赖，并且无法覆盖 `torch` 路径。

### 方案 C：在 `PointCloud` 上挂实例方法

不采用。当前更需要稳定、可组合的模块级函数，而不是继续扩大几何数据模型的职责。

## 风险与回滚

- 风险：SciPy 快路径与 dense 路径数值口径不一致
  - 缓解：为同一输入增加结果一致性测试
- 风险：自动快路径让用户误以为基础功能依赖 SciPy
  - 缓解：在安装说明与 API 文档中明确 SciPy 仅为可选加速
- 风险：批量输入在 SciPy 路径下行为与 dense 路径不一致
  - 缓解：以“逐 batch 样本建树并查询”的方式实现，并添加 batched 测试
- 回滚方式：若 SciPy 路径出现问题，可移除 `_scipy.py` 自动选择逻辑，保留 dense 实现与公开 API 不变

## 验证计划

- 运行 `ruff check .`
- 运行 `pytest`
- 运行 `mkdocs build`
- 检查 `qrlib.metrics` 可直接导入公开函数
- 检查公开文档导航包含 `metrics` 页面，开发者文档仍不进入公开导航
