"""几何模块内部使用的类型别名。"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, TypeAlias

import numpy as np

try:
    import torch as _torch
except ImportError:  # pragma: no cover - 运行时允许无 torch 环境
    _torch = None

if TYPE_CHECKING:
    import torch

    TorchTensor: TypeAlias = torch.Tensor
else:
    if _torch is None:

        class TorchTensor:  # pragma: no cover - 只为运行时类型别名占位
            """torch.Tensor 缺失时的占位类型。"""

    else:
        TorchTensor = _torch.Tensor

ArrayLike: TypeAlias = np.ndarray | TorchTensor
FaceArrayLike: TypeAlias = ArrayLike
VectorLike: TypeAlias = ArrayLike | Sequence[float]
ScaleLike: TypeAlias = ArrayLike | float

__all__ = [
    "ArrayLike",
    "FaceArrayLike",
    "ScaleLike",
    "TorchTensor",
    "VectorLike",
]
