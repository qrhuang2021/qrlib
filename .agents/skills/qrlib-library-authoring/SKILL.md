---
name: qrlib-library-authoring
description: Use when adding or modifying Python library code under src/qrlib. Start from an existing or new developer spec/design, keep public API boundaries explicit, separate internal modules from stable exports, and update tests plus public docs together. Do not use for pure Git workflow tasks or read-only explanation tasks.
---

1. 先确认本次改动对应的 `change slug`，并指出它对应的规范与设计文档路径：
   - `docs/developer/specs/<slug>.md`
   - `docs/developer/design/<slug>.md`

2. 若改动影响公开能力、行为语义、模块边界或目录结构，不要直接写实现；先补齐或更新规范与设计，再进入代码阶段。

3. 识别本次改动的稳定能力边界。新增代码优先落在 `src/qrlib` 下与该能力最匹配的模块或子包中，不要为一次性脚本、薄包装层或实验逻辑创建长期公共模块。

4. 公开接口与内部实现要分层：
   - 稳定公开接口从 `qrlib.<subpackage>` 暴露
   - 内部实现优先使用 `_` 前缀模块
   - `qrlib.__init__` 保持精简

5. 文档也要分层：
   - 面向用户的说明放在 `docs/tutorials/`、`docs/api/`、`docs/concepts/`
   - 面向维护者的规范与设计放在 `docs/developer/`
   - 不要把维护者细节混进公开导航结构

6. 每个 Python 文件只承载一个清晰职责。若一个文件开始同时承担数据模型、后端适配、输入校验与公开 API，优先考虑拆分；但也不要把逻辑切成过度零碎的文件。

7. 注释、文档字符串与说明文档使用中文。注释重点说明设计意图、输入输出约束、边界行为和兼容性，不做逐行翻译。

8. 修改对外公开、稳定承诺的 API 时，必须同步更新：
   - 单元测试与集成测试
   - 相关公开文档
   - 对应的维护者规范与设计

9. 任何重要逻辑、易错分支、形状变换、数值行为、广播约束或 numpy / torch 兼容路径，都必须被测试直接或间接覆盖。

10. 完成前，运行 `./scripts/check.sh`，或等价执行：
    - `ruff check .`
    - `pytest`
    - `mkdocs build`

11. 输出结果时，说明：
    - 本次改动对应的 `change slug`
    - 涉及的公开接口
    - 更新过的规范 / 设计 / 公开文档路径
    - 新增或强化的测试覆盖点
