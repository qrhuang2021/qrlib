# qrlib 文档

`qrlib` 是一个面向三维深度学习项目的可复用 Python 库，用来沉淀跨项目稳定复用的基础能力。

这个文档站面向两类阅读场景：

- 想快速了解库的定位、边界和稳定导入方式
- 想直接查几何能力与指标能力的用法、约束与返回值约定

## 快速入口

- [快速开始](getting-started.md)：安装、校验命令和本地文档预览方式
- [教程总览](tutorials/index.md)：按使用场景组织的完整用法示例
- [API 总览](api/index.md)：稳定公开接口与导入边界
- [概念总览](concepts/index.md)：仓库定位、模块边界与开发范式

## 这个库适合放什么

- 跨项目复用的数据处理能力
- 点云、网格、归一化等稳定几何能力
- 小而稳定、已经被多个项目验证过的指标与辅助模块

## 这个库不适合放什么

- 只服务单个实验或单篇论文的训练流程
- 私有数据、权重、日志、notebook 输出
- 边界不清、持续膨胀的 `utils.py`
- 尚未稳定的一次性代码

## 一个最小示例

```python
import numpy as np

from qrlib.geometry import PointCloud, normalize_to_sphere

points = np.array([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]], dtype=np.float32)
cloud = PointCloud(points)

normalized_cloud, source_center, source_scale = normalize_to_sphere(cloud)
```

如果你想看完整工作流，请继续阅读 [几何归一化工作流](tutorials/geometry-normalization-workflow.md)。
如果你想看点云距离指标的使用方式，请继续阅读 [点云距离指标工作流](tutorials/point-cloud-metrics-workflow.md)。
