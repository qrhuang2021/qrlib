# 快速开始

## 安装

推荐先克隆仓库，再使用 `uv` 配置本地开发环境：

```bash
git clone git@github.com:qrhuang2021/qrlib.git
cd qrlib
uv venv --python 3.11
source .venv/bin/activate
uv pip install --python .venv/bin/python -e ".[dev]"
```

## 统一校验

安装完成后，优先运行仓库统一校验脚本：

```bash
./scripts/check.sh
```

这个脚本会依次执行：

```bash
ruff check .
pytest
mkdocs build
```

## 本地预览文档

这个仓库使用 `MkDocs + Material for MkDocs`：

```bash
mkdocs serve
```

启动后访问 `http://127.0.0.1:8000`。

如果你只是想生成静态站点，可以执行：

```bash
mkdocs build
```

生成完成后，可以直接打开仓库根目录的 `open-docs.html`。这个入口页同时提供：

- 公开文档入口
- 隐藏的开发者规范入口
- 隐藏的开发者设计入口

## 稳定导入建议

建议按能力边界从子包导入，而不是依赖一个很大的顶层导出：

```python
from qrlib.data import ...
from qrlib.geometry import ...
from qrlib.metrics import ...
```

`qrlib.__init__` 会尽量保持精简，避免公共接口失控。

## 下一步阅读

- [几何归一化工作流](tutorials/geometry-normalization-workflow.md)
- [qrlib.geometry API](api/geometry.md)
- [仓库架构](concepts/architecture.md)
- [面向规范开发](concepts/spec-driven-development.md)
