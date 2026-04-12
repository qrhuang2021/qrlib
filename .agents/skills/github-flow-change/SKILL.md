---
name: github-flow-change
description: Use when the task involves modifying files in this repository and preparing the work as a GitHub Flow change, including syncing local `main` with `origin/main`, recommending a branch name, planning local commit boundaries, grouping related local commits into a single PR, cleaning up the local branch after merge, and drafting a PR-ready summary. Do not use for read-only explanation tasks.
---

1. 在开始实施前，先用一句话概括这次改动的单一目标。

2. 在开始开发前，先同步主线：
   - 切换到 `main`。
   - 获取远端更新，并让本地 `main` 与 `origin/main` 保持一致。
   - 不要基于落后的本地 `main` 创建新分支。
   - 如果本地 `main` 有未同步或额外提交，先显式处理，再继续开发。

3. 基于该目标，始终先给出一个推荐 branch 名称。
   - 使用小写 ASCII 和 kebab-case。
   - 名称应短、可读、能直接描述改动目标。
   - 只有在能提升可读性时，才使用 `feature/`、`fix/`、`refactor/`、`docs/`、`test/`、`chore/` 前缀。
   - 如果已知 issue 编号，可把编号加入 branch 名称。

4. 遵循 GitHub Flow：
   - 假定改动应基于与 `origin/main` 同步后的 `main` 切出的短生命周期 topic branch 进行。
   - 一个 branch 只承载一个清晰目标。
   - 不相关改动必须拆分为不同 branch。
   - 一个清晰目标最终对应一个 PR，而不是每个 commit 对应一个 PR。

5. 先规划 commit 边界，再组织代码修改。每个 commit 都应是一个“独立且完整”的改动，便于 review、revert 和 cherry-pick。

6. 推荐 commit message 时，优先使用简洁的 Conventional Commits 风格：
   - `feat: ...`
   - `fix: ...`
   - `refactor: ...`
   - `docs: ...`
   - `test: ...`
   - `chore: ...`
   - 类型前缀使用英文，主题可用中文或英文，但必须简洁且紧扣改动范围。
   - 第一行尽量控制在 50 个字符以内。

7. 如果这次改动天然包含多个独立步骤，主动给出“建议的 commit 划分”和每个 commit 的 message，而不是只给一个总 message。

8. PR 组织方式：
   - 允许在同一个 topic branch 上进行多次本地 commit。
   - 不要因为产生了一个新的本地 commit，就立即创建或更新一个新的 PR。
   - 只有当该 branch 所承载的单一目标已经完整、可 review、并且检查通过后，再创建一个 PR。
   - 同一个 PR 应汇总该 branch 上为达成该目标所做的相关 commit。
   - 若中途出现与当前目标无关的改动，应移到新的 branch，并为其准备单独的 PR。

9. 在认为改动已可提交前，实际运行：
   - `ruff check .`
   - `pytest`
   - 若检查失败，先修复问题或明确记录阻塞项，再决定是否进入 PR 阶段。

10. PR 成功合并后，执行收尾清理：
   - 切回 `main`。
   - 再次同步本地 `main` 与 `origin/main`，确保主线保持最新。
   - 删除本地已合并的 topic branch，避免残留陈旧分支。
   - 只有在确认 PR 已成功合并后，才删除本地分支。

11. 最终输出时，至少给出：
   - 推荐 branch 名称
   - 建议的 commit 划分
   - 每个 commit 的 message
   - 一段可直接用于 PR 描述的变更摘要