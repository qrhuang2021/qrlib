# 快速开始

## 安装

推荐先克隆仓库，再使用 `uv` 配置本地开发环境：

```bash
git clone git@github.com:qrhuang2021/qrlib.git
cd qrlib
uv venv --python 3.11
source .venv/bin/activate
uv pip install --python .venv/bin/python -e ".[dev]"
```

安装完成后，可先运行基础检查：

```bash
ruff check .
pytest
```

## 本地预览 HTML 文档站

这个仓库已经接入 `MkDocs + Material for MkDocs`。本地预览方式如下：

```bash
mkdocs serve
```

启动后访问 `http://127.0.0.1:8000`，可以通过左侧导航、站内搜索和页面目录阅读文档。

如果你只想验证文档能否成功构建，可以执行：

```bash
mkdocs build
```

## 导入建议

建议按能力边界从子包导入，而不是依赖一个很大的顶层导出：

```python
from qrlib.data import ...
from qrlib.geometry import ...
from qrlib.metrics import ...
```

`qrlib.__init__` 会尽量保持精简，避免公共接口失控。

## Geometry 示例

```python
import numpy as np

from qrlib.geometry import PointCloud, normalize_to_sphere

points = np.array(
    [
        [0.0, 0.0, 0.0],
        [2.0, 0.0, 0.0],
        [1.0, 1.0, 0.0],
    ],
    dtype=np.float32,
)
cloud = PointCloud(points)

normalized_cloud, source_center, source_scale = normalize_to_sphere(cloud)
```

更多说明可继续阅读：

- [架构说明](architecture.md)
- [Geometry 总览](geometry/index.md)
- [归一化接口说明](geometry/normalization.md)
