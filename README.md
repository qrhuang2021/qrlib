# qrlib

`qrlib` 是一个面向三维深度学习项目的可复用 Python 库，用来沉淀跨项目稳定复用的基础能力。

- 在线文档：https://qrhuang2021.github.io/qrlib/

## 仓库定位

这个仓库坚持“库优先”而不是“实验工程优先”：

- 只接收稳定、通用、跨项目复用的能力
- 具体训练流程仍然留在各自项目仓库中
- 一段代码至少已经在多个项目里复用过，才适合迁入 `qrlib`

适合放入 `qrlib` 的内容包括：

- 通用数据处理能力，例如采样、`collate`、增强、格式转换
- 几何表示与几何变换，例如点云、网格、归一化
- 可复用的指标计算代码
- 小而稳定、已经被多个项目验证过的辅助模块

不适合放入 `qrlib` 的内容包括：

- 只服务单篇论文或单个实验的完整训练工程
- 私有数据、模型权重、日志与 notebook 输出
- 边界不清、不断膨胀的 `utils.py`
- 只使用过一次、接口仍然频繁变化的代码

## 面向规范开发工作流

本仓库默认按照“规范 -> 设计 -> 实现 -> 验证”的顺序协作开发。

1. 先为本次改动选择一个 `change slug`
2. 在 `docs/developer/specs/<slug>.md` 里写清楚目标、非目标、公开契约与验收标准
3. 在 `docs/developer/design/<slug>.md` 里写清楚模块拆分、实现路径、替代方案与验证计划
4. 再修改 `src/qrlib`、测试和公开文档
5. 最后运行 `./scripts/check.sh`

维护者文档会被构建进文档站，但默认不会出现在公开导航栏中。
如果你想直接打开隐藏入口，可以：

- 本地构建后打开仓库根目录的 `open-docs.html`
- 直接访问 `site/developer/specs/index.html`
- 直接访问 `site/developer/design/index.html`

## 安装

推荐先克隆仓库，再使用 `uv` 配置本地开发环境：

```bash
git clone git@github.com:qrhuang2021/qrlib.git
cd qrlib
uv venv --python 3.11
source .venv/bin/activate
uv pip install --python .venv/bin/python -e ".[dev]"
```

如果你希望为 `numpy` 指标计算启用 SciPy `KDTree` 快路径，可以使用：

```bash
uv pip install --python .venv/bin/python -e ".[dev,scipy]"
```

安装完成后，可以直接运行统一校验脚本：

```bash
./scripts/check.sh
```

如果你只想直接安装这个库，也可以使用：

```bash
uv pip install git+ssh://git@github.com/qrhuang2021/qrlib.git
```

## 文档结构

仓库文档按公开文档与维护者文档分层：

```text
docs/
├─ index.md
├─ getting-started.md
├─ tutorials/
├─ api/
├─ concepts/
└─ developer/
   ├─ specs/
   └─ design/
```

- `tutorials/`：按使用场景组织的教程
- `api/`：稳定公开接口的参考说明
- `concepts/`：仓库定位、模块边界、开发范式
- `developer/`：维护者用的规范与设计，默认不进入公开导航

## 稳定导入方式

建议按能力边界从子包导入，而不是依赖一个很大的顶层导出：

```python
from qrlib.data import ...
from qrlib.geometry import ...
from qrlib.metrics import ...
```

`qrlib.__init__` 会尽量保持精简，避免公共接口失控。

例如，几何归一化接口推荐这样使用：

```python
import numpy as np

from qrlib.geometry import PointCloud, normalize_to_sphere

points = np.array([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]], dtype=np.float32)
cloud = PointCloud(points)

normalized_cloud, source_center, source_scale = normalize_to_sphere(cloud)
```

点云距离指标推荐这样使用：

```python
import numpy as np

from qrlib.metrics import chamfer_distance, hausdorff_distance

source = np.array([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]], dtype=np.float32)
target = np.array([[0.0, 0.0, 0.0]], dtype=np.float32)

cd_score = chamfer_distance(source, target)
hd_score = hausdorff_distance(source, target, directed=True)
```

完整使用流程见 `examples/geometry_workflow.py` 与 `examples/metrics_workflow.py`，公开文档入口见 `docs/`，维护者规范入口见 `docs/developer/`。
