# API 总览

`qrlib` 当前刻意保持精简的公开 API 面：

- 顶层包 `qrlib` 只暴露版本等极少数顶层元信息
- 稳定能力从子包边界暴露，例如 `qrlib.geometry`
- 内部 `_` 前缀模块不属于稳定公开契约

当前主要公开能力：

- [qrlib.geometry](geometry.md)
- [qrlib.metrics](metrics.md)

随着能力增加，这一层会继续收敛稳定入口，而不是把实现细节直接暴露出去。
