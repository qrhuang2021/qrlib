---
name: github-flow-change
description: Use when the task involves modifying files in this repository and preparing the work as a GitHub Flow change. The change should follow qrlib's spec-driven workflow: decide a change slug, sync local main with origin/main, recommend a branch name, plan commit boundaries, and prepare a PR-ready summary that references spec/design docs. Do not use for read-only explanation tasks.
---

1. 在开始实施前，先用一句话概括这次改动的单一目标，并给出建议的 `change slug`。

2. 先判断这次改动是否需要完整规范与设计。只要它影响公开能力、行为、架构、文档结构或协作流程，就应在开始编码前准备：
   - `docs/developer/specs/<slug>.md`
   - `docs/developer/design/<slug>.md`

3. 在开始开发前，同步主线：
   - 切换到 `main`
   - 获取远端更新，并让本地 `main` 与 `origin/main` 保持一致
   - 不要基于落后的本地 `main` 创建新分支
   - 如果本地 `main` 有未同步或额外提交，先显式处理

4. 基于该目标，给出推荐 branch 名称：
   - 使用小写 ASCII 和 kebab-case
   - 名称应短、可读、能直接表达改动目标
   - 可按需要添加 `feature/`、`fix/`、`refactor/`、`docs/`、`test/`、`chore/` 前缀
   - 若合适，尽量让 branch 名称与 `change slug` 对齐

5. 遵循 GitHub Flow：
   - 一个 short-lived topic branch 只承载一个清晰目标
   - 一个清晰目标最终对应一个 PR
   - 与当前目标无关的改动必须拆分到新 branch

6. 先规划 commit 边界，再组织修改。每个 commit 都应独立、完整、便于 review、revert 和 cherry-pick。

7. 推荐 commit message 时，优先使用简洁的 Conventional Commits 风格：
   - `feat: ...`
   - `fix: ...`
   - `refactor: ...`
   - `docs: ...`
   - `test: ...`
   - `chore: ...`

8. 如果改动天然包含多个步骤，主动给出“建议的 commit 划分”，并明确哪些 commit 对应规范 / 设计，哪些 commit 对应实现 / 测试 / 文档。

9. 进入 PR 阶段前，实际运行 `./scripts/check.sh`，或等价执行：
   - `ruff check .`
   - `pytest`
   - `mkdocs build`

10. PR 成功合并后，执行收尾：
    - 切回 `main`
    - 再次同步本地 `main` 与 `origin/main`
    - 删除本地已合并的 topic branch

11. 最终输出时，至少给出：
    - `change slug`
    - 规范与设计路径
    - 推荐 branch 名称
    - 建议的 commit 划分
    - 每个 commit 的 message
    - 一段可直接用于 PR 描述的变更摘要
