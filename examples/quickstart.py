"""演示外部项目如何导入 qrlib。"""

from qrlib import __version__, data, geometry, metrics


def main() -> None:
    print(f"qrlib 版本: {__version__}")
    print(f"已导入包: {data.__name__}")
    print(f"已导入包: {geometry.__name__}")
    print(f"已导入包: {metrics.__name__}")
    print("通用的数据处理代码建议放在 qrlib.data 下。")
    print("稳定的几何类型与几何变换建议放在 qrlib.geometry 下。")
    print("通用的指标计算代码建议放在 qrlib.metrics 下。")
    print("几何完整使用示例见 examples/geometry_workflow.py。")


if __name__ == "__main__":
    main()
