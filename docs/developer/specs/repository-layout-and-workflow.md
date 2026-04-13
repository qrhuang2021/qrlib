# 规范：仓库布局与协作工作流

- `change slug`：`repository-layout-and-workflow`
- 状态：`accepted`
- 负责人：qrlib maintainers

## 背景

原仓库已经有文档、测试与 AGENTS/skills，但整体仍然偏“实现优先、文档补充”。
为了让下一次 Codex 协作开发能够直接延续同一范式，需要把规范、设计、实现、验证明确拆开。

## 目标

- 将文档结构调整为公开文档与维护者文档分层
- 让 `developer` 文档默认不出现在公开导航中，但仍可直接访问
- 让 AGENTS 和 skills 明确采用“规范 -> 设计 -> 实现 -> 验证”的顺序
- 提供可复用的规范与设计模板
- 让 CI、脚本与测试共同约束这套结构

## 非目标

- 不引入新的复杂文档插件体系
- 不把所有维护者细节暴露到公开导航
- 不为每个微小改动强制生成新文档

## 公开契约

- `docs/` 目录必须包含：
  - `index.md`
  - `getting-started.md`
  - `tutorials/`
  - `api/`
  - `concepts/`
  - `developer/specs/`
  - `developer/design/`
- `mkdocs.yml` 的公开导航中不得出现 `developer`
- 维护者可以通过 `open-docs.html` 或直接 URL 打开 `developer/specs` 与 `developer/design`
- 非微小改动默认需要维护者规范与设计文档
- 统一校验命令为 `./scripts/check.sh`

## 验收标准

- 文档目录结构符合约定
- `open-docs.html` 同时提供公开文档和隐藏开发者入口
- `AGENTS.md` 与相关 `SKILL.md` 已同步到面向规范开发范式
- 集成测试能验证文档布局与隐藏入口
- `./scripts/check.sh`、CI、`pytest`、`mkdocs build` 能一起工作

## 兼容性与迁移

- 公开文档导航发生重组，但功能说明仍保持连续
- 维护者文档从公开导航移除，改为隐藏直达入口
