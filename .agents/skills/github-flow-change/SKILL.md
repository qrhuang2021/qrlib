---
name: github-flow-change
description: Use when the task involves modifying files in this repository and preparing the work as a GitHub Flow change, including recommending a branch name, planning commit boundaries, proposing commit messages, and drafting a PR-ready summary. Do not use for read-only explanation tasks.
---

1. 在开始实施前，先用一句话概括这次改动的单一目标。

2. 基于该目标，始终先给出一个推荐 branch 名称。
   - 使用小写 ASCII 和 kebab-case。
   - 名称应短、可读、能直接描述改动目标。
   - 只有在能提升可读性时，才使用 `feature/`、`fix/`、`refactor/`、`docs/`、`test/`、`chore/` 前缀。
   - 如果已知 issue 编号，可把编号加入 branch 名称。

3. 遵循 GitHub Flow：
   - 假定改动应基于 `main` 的短生命周期 topic branch 进行。
   - 一个 branch 只承载一个清晰目标。
   - 不相关改动必须拆分为不同 branch。

4. 先规划 commit 边界，再组织代码修改。每个 commit 都应是一个“独立且完整”的改动，便于 review、revert 和 cherry-pick。

5. 推荐 commit message 时，优先使用简洁的 Conventional Commits 风格：
   - `feat: ...`
   - `fix: ...`
   - `refactor: ...`
   - `docs: ...`
   - `test: ...`
   - `chore: ...`
   - 类型前缀使用英文，主题可用中文或英文，但必须简洁且紧扣改动范围。
   - 第一行尽量控制在 50 个字符以内。

6. 如果这次改动天然包含多个独立步骤，主动给出“建议的 commit 划分”和每个 commit 的 message，而不是只给一个总 message。

7. 在认为改动已可提交前，实际运行：
   - `ruff check .`
   - `pytest`

8. 最终输出时，至少给出：
   - 推荐 branch 名称
   - 建议的 commit 划分
   - 每个 commit 的 message
   - 一段可直接用于 PR 描述的变更摘要