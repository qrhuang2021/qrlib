# AGENTS.md

## 当前状态

- 包目录在 `src/qrlib`
- 当前只有 `qrlib.data` 和 `qrlib.metrics`

## 协作约定

- 与用户沟通使用中文
- 代码注释、文档字符串、说明文档使用中文
- 注释保持简洁，重点解释设计意图、输入输出和边界，不做逐行翻译
- `qrlib.__init__` 保持精简
- 每个 Python 文件只承载一个明确能力
- 优先使用少量职责清晰的类做模块化设计
- 不要把逻辑拆成很多很小、很碎的函数
- 每个 Python 文件都要明确对外开放的接口
- 内部使用的函数或类使用 `_` 前缀，与对外接口区分开

## 本地开发

```bash
git clone git@github.com:qrhuang2021/qrlib.git
cd qrlib
uv venv --python 3.11
source .venv/bin/activate
uv pip install --python .venv/bin/python -e ".[dev]"
ruff check .
pytest
```
