# qrlib 文档

`qrlib` 是一个面向三维深度学习项目的可复用 Python 库，用来沉淀跨项目稳定复用的基础能力。

这个文档站面向两类阅读场景：

- 想快速判断一段能力是否适合迁入 `qrlib`
- 想直接查公开接口、几何约束和使用方式

## 适合放入 `qrlib` 的内容

- 数据处理相关的通用代码，例如采样、`collate`、增强、格式转换
- 几何表示与几何变换，例如点云、网格、归一化
- 可复用的指标计算代码
- 小而稳定、已经在多个项目中复用的辅助模块

## 不适合放入 `qrlib` 的内容

- 完整实验流程或只服务某一篇论文的训练代码
- 私有数据、模型权重、日志、依赖本地路径的 notebook
- 把各种无关函数都塞进去的 `utils.py`
- 只用过一次、接口还不稳定的代码

## 快速入口

- [快速开始](getting-started.md)：安装、导入建议和本地预览文档站
- [架构说明](architecture.md)：仓库定位、模块边界和代码迁入规则
- [Geometry 总览](geometry/index.md)：当前公开几何接口与使用约束

## 一个最小示例

```python
import numpy as np

from qrlib.geometry import PointCloud, normalize_to_sphere

points = np.array([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]], dtype=np.float32)
cloud = PointCloud(points)

normalized_cloud, source_center, source_scale = normalize_to_sphere(cloud)
```

如果你想看完整工作流，可以参考仓库根目录下的 `examples/geometry_workflow.py`。
