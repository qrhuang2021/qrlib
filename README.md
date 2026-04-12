# qrlib

`qrlib` 是一个面向三维深度学习项目的可复用 Python 库，用来沉淀跨项目稳定复用的代码。

这个仓库以“库优先”为原则：

- 把稳定、通用、跨项目复用的代码放进来
- 具体任务的训练工程仍然放在各自项目仓库中
- 一段代码至少在两个项目中复用后，再考虑迁入 `qrlib`

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

## 安装

先通过 Git SSH 地址获取仓库，再使用 `uv` 配置本地开发环境：

```bash
git clone git@github.com:qrhuang2021/qrlib.git
cd qrlib
uv venv --python 3.11
source .venv/bin/activate
uv pip install --python .venv/bin/python -e ".[dev]"
```

安装完成后可执行基础检查：

```bash
ruff check .
pytest
```

如果你的项目环境里已经安装了 `torch`，`qrlib.geometry` 会自动支持 `torch.Tensor` 路径。
这里不把 `torch` 声明为库本身的安装依赖，避免在不同平台上强行绑定具体的 PyTorch 分发方式。

如果你只是想直接安装这个库，也可以使用：

```bash
uv pip install git+ssh://git@github.com/qrhuang2021/qrlib.git
```

## 目录概览

```text
qrlib/
├─ pyproject.toml
├─ src/qrlib/
│  ├─ data/
│  ├─ geometry/
│  ├─ metrics/
├─ tests/
├─ examples/
├─ docs/
└─ scripts/
```

## 导入方式

建议按能力边界从子包导入，而不是依赖一个很大的顶层导出：

```python
from qrlib.data import ...
from qrlib.geometry import ...
from qrlib.metrics import ...
```

`qrlib.__init__` 会尽量保持精简，避免公共接口失控。

例如，几何归一化接口推荐这样使用：

```python
import numpy as np

from qrlib.geometry import PointCloud, normalize_to_sphere

points = np.array([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]], dtype=np.float32)
cloud = PointCloud(points)

normalized_cloud, source_center, source_scale = normalize_to_sphere(cloud)
```

`qrlib.geometry` 的公开说明集中放在 `docs/geometry/` 下：

- [docs/geometry/index.md](docs/geometry/index.md)：总览、类型约束与基础使用方式
- [docs/geometry/normalization.md](docs/geometry/normalization.md)：归一化与反归一化行为说明

`examples` 按使用场景组织，不按单个源码文件逐一配套。当前几何能力对应一个统一示例：

- [examples/geometry_workflow.py](examples/geometry_workflow.py)

## 新代码迁入规则

在把代码放进 `qrlib` 之前，先问自己三个问题：

1. 这段代码是否已经在多个项目中复用？
2. 它的接口是否已经足够稳定，能让别人依赖？
3. 它是否自然属于一个边界清晰、文档化的稳定子包，例如 `qrlib.data`、`qrlib.geometry` 或 `qrlib.metrics`？

如果答案是否定的，就先继续留在具体项目仓库里。

新增能力时，不要求为每个源码文件机械补齐一份独立文档和示例。
更重要的是：

- 对外公开、稳定承诺的 API 有充分测试
- 用户能在 `docs/` 中找到必要说明
- `examples/` 能覆盖真实使用场景
- 重要边界、形状变换和数值行为能被测试验证

更多说明见 [docs/architecture.md](docs/architecture.md)。
