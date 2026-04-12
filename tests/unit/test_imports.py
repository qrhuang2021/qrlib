import importlib

import pytest

import qrlib


def test_package_version_is_exposed() -> None:
    assert qrlib.__version__ == "0.1.0"


@pytest.mark.parametrize(
    "module_name",
    [
        "qrlib.data",
        "qrlib.geometry",
        "qrlib.metrics",
    ],
)
def test_core_subpackages_import(module_name: str) -> None:
    module = importlib.import_module(module_name)
    assert module.__name__ == module_name
