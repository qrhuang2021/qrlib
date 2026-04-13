# 设计：仓库布局与协作工作流

- `change slug`：`repository-layout-and-workflow`
- 对应规范：`../specs/repository-layout-and-workflow.md`

## 总体方案

采用“公开文档 + 隐藏维护者文档 + 统一校验脚本 + AGENTS/skills 约束 + 集成测试校验”的组合方式，而不是引入额外复杂工具链。

## 模块与文件落点

### 文档层

- 公开文档：
  - `docs/index.md`
  - `docs/getting-started.md`
  - `docs/tutorials/`
  - `docs/api/`
  - `docs/concepts/`
- 维护者文档：
  - `docs/developer/specs/`
  - `docs/developer/design/`

### 协作约束层

- `AGENTS.md`：仓库级工作流约束
- `.agents/skills/qrlib-spec-driven-change/SKILL.md`：规范优先入口
- `.agents/skills/qrlib-library-authoring/SKILL.md`：库代码实现约束
- `.agents/skills/github-flow-change/SKILL.md`：分支、commit、PR 组织方式

### 验证层

- `scripts/check.sh`：统一校验入口
- `.github/workflows/ci.yml`：在 CI 中复用统一脚本
- `tests/integration/test_repository_contract.py`：验证文档布局、隐藏入口与 skill 入口

## 为什么这样设计

- MkDocs 本身就支持构建未出现在导航中的页面，不需要额外插件也能满足“默认不显示 developer，但可直接访问”
- 使用 `open-docs.html` 提供显式入口，比要求维护者自己拼 URL 更简单
- 用测试校验仓库结构，可以避免未来重构时悄悄破坏这套工作流

## 备选方案与取舍

### 方案 A：把 developer 文档完全排除出站点

不采用。因为这样虽然隐藏得更彻底，但维护者每次都只能回 GitHub 仓库看 Markdown，不利于统一入口。

### 方案 B：把 developer 文档直接放入公开导航

不采用。因为会把维护者细节和用户文档混在一起，降低外部文档清晰度。

## 风险与缓解

- 风险：未来有人在 `mkdocs.yml` 里直接把 `developer` 加回导航
  - 缓解：集成测试直接检查导航配置
- 风险：维护者不知道隐藏入口怎么打开
  - 缓解：`open-docs.html` 与 `README.md` 同时提供入口说明

## 验证计划

- 运行 `./scripts/check.sh`
- 确认 `mkdocs build` 可以构建隐藏维护者页面
- 确认 `open-docs.html` 包含 `developer/specs` 与 `developer/design` 的直达链接
