# qrlib

`qrlib` 是一个面向三维深度学习项目的可复用 Python 库，用来沉淀跨项目稳定复用的代码。

这个仓库以“库优先”为原则：

- 把稳定、通用、跨项目复用的代码放进来
- 具体任务的训练工程仍然放在各自项目仓库中
- 一段代码至少在两个项目中复用后，再考虑迁入 `qrlib`

## 适合放入 `qrlib` 的内容

- 数据处理相关的通用代码，例如归一化、采样、`collate`、增强
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
│  ├─ metrics/
├─ tests/
├─ examples/
├─ docs/
└─ scripts/
```

## 导入方式

建议显式从子包导入，而不是依赖一个很大的顶层导出：

```python
from qrlib.data import ...
from qrlib.metrics import ...
```

`qrlib.__init__` 会尽量保持精简，避免公共接口失控。

## 新代码迁入规则

在把代码放进 `qrlib` 之前，先问自己三个问题：

1. 这段代码是否已经在多个项目中复用？
2. 它的接口是否已经足够稳定，能让别人依赖？
3. 它是否自然属于 `qrlib.data` 或 `qrlib.metrics`？

如果答案是否定的，就先继续留在具体项目仓库里。

更多说明见 [docs/architecture.md](docs/architecture.md)。
