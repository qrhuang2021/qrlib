# 规范：几何归一化

- `change slug`：`geometry-normalization`
- 状态：`accepted`
- 负责人：qrlib maintainers

## 背景

几何归一化是 `qrlib.geometry` 的第一批稳定公开能力之一，需要明确它的输入输出契约、数值语义与兼容边界，避免未来重构时无意改变行为。

## 目标

- 为点云、网格和原始坐标数组提供统一的归一化 / 反归一化能力
- 同时支持 `numpy.ndarray` 与可选的 `torch.Tensor`
- 保持输入类型与输出类型一致
- 对网格只变换顶点，不改写面索引
- 支持 batched 点坐标

## 非目标

- 不处理文件读写
- 不处理网格拓扑编辑
- 不负责训练流程中的数据集与 batch 管理

## 公开契约

### 数据类型

- `PointCloud(points)`：`points` 必须为 `(N, 3)` 或 `(..., N, 3)`
- `Mesh(vertices, faces)`：
  - `vertices` 必须为 `(N, 3)` 或 `(..., N, 3)`
  - `faces` 必须为二维整数矩阵，且 `K >= 3`
  - `vertices` 与 `faces` 必须来自同一后端族

### 函数

- `normalize_to_sphere(data, center=(0, 0, 0), radius=1.0, eps=1e-8)`
- `normalize_to_cube(data, center=(0, 0, 0), edge_length=2.0, eps=1e-8)`
- `normalize(data, center, scale, eps=1e-8)`
- `denormalize(data, center, scale, eps=1e-8)`

### 返回值与语义

- 输入数组返回数组，输入 `PointCloud` 返回 `PointCloud`，输入 `Mesh` 返回 `Mesh`
- `normalize_to_sphere` 返回点坐标均值中心与最大欧氏距离
- `normalize_to_cube` 返回包围盒中心与最大半边长
- `normalize` / `denormalize` 使用显式 `center` 与 `scale`

### 错误语义

以下情况必须显式报错：

- 非法坐标 shape
- 非法面索引 shape 或 dtype
- `numpy` / `torch` 混用
- `radius`、`edge_length` 或 `scale` 小于最小阈值
- `center` 或 `scale` 不可广播到输入批次维度

## 验收标准

- numpy 路径测试通过
- torch 路径测试通过（若环境安装 torch）
- `PointCloud` / `Mesh` 的方法路径与模块级函数一致
- 面索引在变换前后保持不变
- 广播错误会抛出明确异常

## 兼容性与迁移

- 公开导入路径保持为 `from qrlib.geometry import ...`
- 兼容从 `qrlib.geometry.types` 访问类型对象
