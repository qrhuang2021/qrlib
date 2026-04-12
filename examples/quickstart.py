"""演示外部项目如何导入 qrlib。"""

from qrlib import __version__, data, metrics


def main() -> None:
    print(f"qrlib 版本: {__version__}")
    print(f"已导入包: {data.__name__}")
    print(f"已导入包: {metrics.__name__}")
    print("通用的数据处理代码建议放在 qrlib.data 下。")
    print("通用的指标计算代码建议放在 qrlib.metrics 下。")


if __name__ == "__main__":
    main()
