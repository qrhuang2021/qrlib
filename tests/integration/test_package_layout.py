from pathlib import Path

import qrlib


def test_src_layout_keeps_expected_subpackages() -> None:
    package_root = Path(qrlib.__file__).resolve().parent
    package_dirs = {
        path.name
        for path in package_root.iterdir()
        if path.is_dir() and not path.name.startswith("__")
    }

    assert {"data", "metrics"}.issubset(package_dirs)
    assert package_dirs == {"data", "metrics"}


def test_top_level_api_stays_small() -> None:
    assert qrlib.__all__ == ["__version__"]
