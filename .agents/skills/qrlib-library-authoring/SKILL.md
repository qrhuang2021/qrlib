
## `.agents/skills/qrlib-library-authoring/SKILL.md`

```md
---
name: qrlib-library-authoring
description: Use when adding or modifying Python library code under src/qrlib, especially when deciding module boundaries, public/private API shape, comments, docstrings, tests, examples, and documentation. Do not use for pure Git workflow tasks or read-only explanation tasks.
---

1. 先识别本次改动对应的领域能力边界。新增代码优先落在 `src/qrlib` 下与该能力最匹配的模块或子包中。

2. 每个 Python 文件只承载一个明确能力。若一个文件开始同时承担多个不相干职责，应考虑拆分；但不要把逻辑拆成很多很小、很碎的函数。

3. 优先使用少量职责清晰的类或模块组织代码，而不是过度分层或过度包装。

4. 每个 Python 文件都要让对外接口清晰可见。内部函数或类使用 `_` 前缀，与对外接口区分。

5. `qrlib.__init__` 保持精简，只导出有意公开、相对稳定的接口。

6. 注释、文档字符串、说明文档使用中文。注释保持简洁，重点解释设计意图、输入输出、约束条件和边界行为，不做逐行翻译。

7. 不要机械地为每个文件单独补齐 `docs`、`examples` 和 `tests`。`examples` 按使用场景组织，同类能力可共享一个示例。

8. 内部实现、私有辅助函数或薄包装层，不要求单独提供面向用户的文档或示例。

9. 对外公开、稳定承诺的 API，必须优先补齐测试，并提供必要文档说明。

10. 任何重要逻辑、易错分支、形状变换、数值计算或边界行为，都必须被测试直接或间接覆盖。

11. 输出结果时，说明本次改动涉及的公开接口、测试覆盖点，以及是否需要补充示例或文档。
```
