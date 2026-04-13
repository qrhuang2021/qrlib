---
name: qrlib-spec-driven-change
description: Use when planning or executing any non-trivial change in qrlib. Decide whether the change needs a full spec/design, create or update docs/developer/specs and docs/developer/design first, then map the change to implementation, tests, public docs, and verification. Do not use for typo-only or read-only tasks.
---

1. 先给本次改动起一个稳定的 `change slug`。slug 应简短、可读、可复用到：
   - `docs/developer/specs/<slug>.md`
   - `docs/developer/design/<slug>.md`
   - branch 名称

2. 判断是否需要完整规范与设计：
   - 只要改动影响公开 API、行为语义、目录结构、架构边界、构建流程、文档结构或协作流程，就需要完整规范与设计。
   - 纯文案修正、纯注释修改、纯测试补全且不改行为，可不新建独立文档，但若触碰已有规范覆盖内容，仍要更新相应文档。

3. 先写规范，再写设计，不要反过来。

4. 规范至少包含：
   - 背景与问题
   - 目标与非目标
   - 公开契约 / 边界 / 约束
   - 验收标准
   - 兼容性与迁移影响

5. 设计至少包含：
   - 与规范对应关系
   - 模块拆分与文件落点
   - 关键数据流或调用流
   - 备选方案与取舍
   - 风险、回滚与验证计划

6. 当规范与设计稳定后，再列出实现清单：
   - 代码文件
   - 测试文件
   - 公开文档
   - 维护者文档
   - 校验命令

7. 若改动涉及公开文档，公开说明写入：
   - `docs/tutorials/`
   - `docs/api/`
   - `docs/concepts/`

8. 若改动涉及维护者工作流、目录结构或开发范式，必须同步更新：
   - `AGENTS.md`
   - 相关 `.agents/skills/*/SKILL.md`

9. 完成后，确认以下一致：
   - 规范描述的契约与代码实现一致
   - 设计文档中的模块拆分与实际文件结构一致
   - 测试覆盖了规范中的验收项
   - 公开文档只暴露用户需要知道的内容，维护者细节留在 `docs/developer/`

10. 交付时，输出：
    - `change slug`
    - 规范路径
    - 设计路径
    - 关键实现文件
    - 验证结果
