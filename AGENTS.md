# AGENTS.md

## 仓库事实

- Python 包根目录为 `src/qrlib`，采用 `src` layout。
- 公开文档与维护者文档分层组织：
  - 对外文档放在 `docs/index.md`、`docs/getting-started.md`、`docs/tutorials/`、`docs/api/`、`docs/concepts/`
  - 维护者规范与设计放在 `docs/developer/specs/` 与 `docs/developer/design/`
- `docs/developer/` 下的页面会被构建进站点，但默认不出现在公开导航栏中；维护者可通过 `open-docs.html` 或直接访问 `/developer/specs/`、`/developer/design/` 打开。
- `qrlib.__init__` 保持精简，只暴露明确承诺的顶层接口。

## 面向规范开发

本仓库默认采用“规范 -> 设计 -> 实现 -> 验证”的工作流。

### 何时必须先写规范与设计

以下改动在动手改代码前，必须先创建或更新同 slug 的维护者文档：

- 新增公开能力或修改公开 API
- 改变已有行为、输入输出约束、错误语义或数值约定
- 影响模块边界、目录结构、构建方式、文档结构或协作流程的重构
- 任何你预期会影响下一次 Codex 协作开发判断的改动

对应文档路径：

- `docs/developer/specs/<change-slug>.md`
- `docs/developer/design/<change-slug>.md`

### 何时可以不新建完整规范

以下小改动可以不新建独立规范，但如果它们触碰已有规范覆盖的内容，仍要同步更新已有规范或设计：

- 纯文案修正
- 注释、示例、测试补全且不改变行为
- 不改变行为的局部内部重命名或整理

### 规范与设计最少应包含什么

规范至少回答：为什么改、要解决什么、不解决什么、公开契约是什么、验收标准是什么。

设计至少回答：准备怎么拆模块、哪些文件会改、为什么这样做、替代方案是什么、如何验证。

## 协作约定

- 与用户沟通、代码注释、文档字符串、说明文档默认使用中文。
- 新增内部实现模块时，优先使用 `_` 前缀，与稳定公开接口区分。
- 修改对外公开、稳定承诺的 API 时，必须同步更新：
  - 测试
  - 公开文档（`docs/tutorials` / `docs/api` / `docs/concepts`）
  - 维护者规范与设计（`docs/developer/specs` / `docs/developer/design`）
- 完成标准不是“文件补齐”，而是公开契约、实现边界、验证方式与文档入口一致。

## 技能使用

- 任何非微小改动，先使用 `qrlib-spec-driven-change`，确定 change slug、规范路径、设计路径与验收标准。
- 修改 `src/qrlib` 下的库代码时，使用 `qrlib-library-authoring`。
- 需要组织 branch、commit 边界、PR 摘要时，使用 `github-flow-change`。

## 验证要求

在宣称任务完成前，必须实际运行以下检查，或运行等价的 `./scripts/check.sh`：

```bash
ruff check .
pytest
mkdocs build
```

## 本地开发

```bash
git clone git@github.com:qrhuang2021/qrlib.git
cd qrlib
uv venv --python 3.11
source .venv/bin/activate
uv pip install --python .venv/bin/python -e ".[dev]"
./scripts/check.sh
```
