# AGENTS.md

## 仓库事实

- Python 包根目录为 `src/qrlib`。
- 新增长期代码时，以稳定领域能力划分子包；不要为一次性脚本、临时实验或薄包装层创建长期子包。
- `qrlib.__init__` 保持精简，只暴露有意对外公开且相对稳定的接口。

## 协作约定

- 在本仓库中，与用户沟通使用中文。
- 代码注释、文档字符串、说明文档使用中文。
- 修改对外公开、稳定承诺的 API 时，必须同步补齐或更新必要测试与说明文档。
- 在宣称任务完成前，必须实际运行：
  - `ruff check .`
  - `pytest`
- 完成标准不是机械补齐文件数，而是让公开能力可理解、可运行、可验证。

## 技能使用

- 新增或修改 `src/qrlib` 下的库代码时，优先使用 `qrlib-library-authoring`。
- 需要按 GitHub Flow 组织改动、推荐 branch 名称、拆分 commit、生成 commit message 或整理 PR 摘要时，优先使用 `github-flow-change`。

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
