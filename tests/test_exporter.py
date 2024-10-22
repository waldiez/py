"""Test WaldieExporter."""

from pathlib import Path

import pytest

from waldiez import Waldie, WaldieExporter
from waldiez.models import WaldieFlow

from .exporting.flow_helpers import get_flow


def test_export_load_from_file(waldie_flow: WaldieFlow) -> None:
    """Test exporting and loading from file.

    Parameters
    ----------
    waldie_flow : WaldieFlow
        A WaldieFlow instance.
    """
    waldie = Waldie(flow=waldie_flow)
    exporter = WaldieExporter(waldie)
    output_file = Path("waldie.waldiez")
    exporter.export(str(output_file))
    assert output_file.exists()
    WaldieExporter.load(output_file)
    output_file.unlink()


def test_exporter_load_invalid_path() -> None:
    """Test exporter load invalid path."""
    with pytest.raises(ValueError):
        WaldieExporter.load(Path("non_existent_file"))


def test_exporter_use_directory(waldie_flow: WaldieFlow) -> None:
    """Test exporter use directory.

    Parameters
    ----------
    waldie_flow : WaldieFlow
        A WaldieFlow instance.
    """
    waldie = Waldie(flow=waldie_flow)
    exporter = WaldieExporter(waldie)
    output_dir = Path("output_dir.waldiez")
    output_dir.mkdir()
    with pytest.raises(IsADirectoryError):
        exporter.export(output_dir)
    output_dir.rmdir()


def test_exporter_file_exists(waldie_flow: WaldieFlow) -> None:
    """Test exporter file exists.

    Parameters
    ----------
    waldie_flow : WaldieFlow
        A WaldieFlow instance.
    """
    waldie = Waldie(flow=waldie_flow)
    exporter = WaldieExporter(waldie)
    output_file = Path("waldie.waldiez")
    output_file.touch()
    with pytest.raises(FileExistsError):
        exporter.export(output_file)
    exporter.export(output_file, force=True)
    output_file.unlink()


def test_exporter_force(waldie_flow: WaldieFlow) -> None:
    """Test exporter force.

    Parameters
    ----------
    waldie_flow : WaldieFlow
        A WaldieFlow instance.
    """
    waldie = Waldie(flow=waldie_flow)
    exporter = WaldieExporter(waldie)
    output_file = Path("waldie.waldiez")
    output_file.touch()
    exporter.export(output_file, force=True)
    output_file.unlink()


def test_export_to_py(waldie_flow: WaldieFlow) -> None:
    """Test exporting to Python.

    Parameters
    ----------
    waldie_flow : WaldieFlow
        A WaldieFlow instance.
    """
    waldie = Waldie(flow=waldie_flow)
    exporter = WaldieExporter(waldie)
    output_file = Path("waldie.py")
    exporter.export(output_file)
    assert output_file.exists()
    output_file.unlink()


def test_export_to_ipynb(waldie_flow: WaldieFlow) -> None:
    """Test exporting to Jupyter Notebook.

    Parameters
    ----------
    waldie_flow : WaldieFlow
        A WaldieFlow instance.
    """
    waldie = Waldie(flow=waldie_flow)
    exporter = WaldieExporter(waldie)
    output_file = Path("waldie.ipynb")
    exporter.export(output_file)
    assert output_file.exists()
    output_file.unlink()


def test_export_to_waldiez(waldie_flow: WaldieFlow) -> None:
    """Test exporting to Waldiez file.

    Parameters
    ----------
    waldie_flow : WaldieFlow
        A WaldieFlow instance.
    """
    waldie = Waldie(flow=waldie_flow)
    exporter = WaldieExporter(waldie)
    output_file = Path("waldie.waldiez")
    exporter.export(output_file)
    assert output_file.exists()
    output_file.unlink()


def test_export_to_invalid_extension(waldie_flow: WaldieFlow) -> None:
    """Test exporting to invalid extension.

    Parameters
    ----------
    waldie_flow : WaldieFlow
        A WaldieFlow instance.
    """
    waldie = Waldie(flow=waldie_flow)
    exporter = WaldieExporter(waldie)
    output_file = Path("waldie.invalid")
    with pytest.raises(ValueError):
        exporter.export(output_file)


def test_export_complex_flow() -> None:
    """Test exporting invalid flow."""
    flow = get_flow()
    waldie = Waldie(flow=flow)
    exporter = WaldieExporter(waldie)
    output_file = Path("waldie.py")
    exporter.export(output_file)
    assert output_file.exists()
    output_file.unlink()
    skill_file = Path("skill_name.py")
    assert skill_file.exists()
    skill_file.unlink()
