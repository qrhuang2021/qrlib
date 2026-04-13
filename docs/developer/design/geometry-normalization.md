# 设计：几何归一化

- `change slug`：`geometry-normalization`
- 对应规范：`../specs/geometry-normalization.md`

## 总体方案

将几何能力拆成“公开 API + 内部模型 + 内部校验 + 后端适配”四层：

- `geometry/__init__.py`：稳定导出面
- `geometry/types.py`：公开类型与兼容层
- `geometry/normalization.py`：公开归一化函数
- `geometry/_models.py`：`PointCloud` 与 `Mesh`
- `geometry/_validation.py`：输入校验
- `geometry/_backend.py`：numpy / torch 后端差异封装
- `geometry/_typing.py`：内部类型别名

## 关键数据流

1. 模块级函数或对象方法接收 `ArrayLike | PointCloud | Mesh`
2. `normalization.py` 使用 `_GeometryAdapter` 统一拆出坐标数组与可选面索引
3. `_backend.py` 负责 dtype 对齐、广播、numpy / torch 运算差异
4. 归一化完成后，`normalization.py` 根据原始输入类型重建数组、点云或网格

## 为什么这样拆分

旧结构里，`types.py` 同时承载类型别名、数据模型和输入校验，`normalization.py` 同时承载公开 API 与后端细节。随着能力增加，这会让责任边界越来越模糊。

现在拆分后：

- 公开 API 更容易识别
- 内部模块职责更单一
- 未来增加新的几何变换时，可以直接复用 `_backend.py` 与 `_validation.py`
- `types.py` 保留为公开兼容层，避免影响既有深层导入路径

## 备选方案与取舍

### 方案 A：继续维持单文件实现

不采用。因为职责继续增长后，后端差异、数据模型与公开 API 会越来越难维护。

### 方案 B：把每个小函数拆成很多更细的文件

不采用。因为当前能力还不大，过度细分会降低可读性。

## 风险与缓解

- 风险：内部重构破坏深层导入路径
  - 缓解：保留 `geometry/types.py` 作为公开兼容层，并添加对应测试
- 风险：广播与 dtype 行为在 numpy / torch 下不一致
  - 缓解：统一收口到 `_backend.py` 并保留双后端测试

## 验证计划

- 运行现有几何单元测试
- 增加公开兼容层与广播错误测试
- 通过集成测试确认包结构不被破坏
