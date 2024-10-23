"""Test WaldiezExporter."""

from pathlib import Path

import pytest

from waldiez import Waldiez, WaldiezExporter
from waldiez.models import WaldiezFlow

from .exporting.flow_helpers import get_flow


def test_export_load_from_file(waldiez_flow: WaldiezFlow) -> None:
    """Test exporting and loading from file.

    Parameters
    ----------
    waldiez_flow : WaldiezFlow
        A WaldiezFlow instance.
    """
    waldiez = Waldiez(flow=waldiez_flow)
    exporter = WaldiezExporter(waldiez)
    output_file = Path("flow.waldiez")
    exporter.export(str(output_file))
    assert output_file.exists()
    WaldiezExporter.load(output_file)
    output_file.unlink()


def test_exporter_load_invalid_path() -> None:
    """Test exporter load invalid path."""
    with pytest.raises(ValueError):
        WaldiezExporter.load(Path("non_existent_file"))


def test_exporter_use_directory(waldiez_flow: WaldiezFlow) -> None:
    """Test exporter use directory.

    Parameters
    ----------
    waldiez_flow : WaldiezFlow
        A WaldiezFlow instance.
    """
    waldiez = Waldiez(flow=waldiez_flow)
    exporter = WaldiezExporter(waldiez)
    output_dir = Path("output_dir.waldiez")
    output_dir.mkdir()
    with pytest.raises(IsADirectoryError):
        exporter.export(output_dir)
    output_dir.rmdir()


def test_exporter_file_exists(waldiez_flow: WaldiezFlow) -> None:
    """Test exporter file exists.

    Parameters
    ----------
    waldiez_flow : WaldiezFlow
        A WaldiezFlow instance.
    """
    waldiez = Waldiez(flow=waldiez_flow)
    exporter = WaldiezExporter(waldiez)
    output_file = Path("flow.waldiez")
    output_file.touch()
    with pytest.raises(FileExistsError):
        exporter.export(output_file)
    exporter.export(output_file, force=True)
    output_file.unlink()


def test_exporter_force(waldiez_flow: WaldiezFlow) -> None:
    """Test exporter force.

    Parameters
    ----------
    waldiez_flow : WaldiezFlow
        A WaldiezFlow instance.
    """
    waldiez = Waldiez(flow=waldiez_flow)
    exporter = WaldiezExporter(waldiez)
    output_file = Path("flow.waldiez")
    output_file.touch()
    exporter.export(output_file, force=True)
    output_file.unlink()


def test_export_to_py(waldiez_flow: WaldiezFlow) -> None:
    """Test exporting to Python.

    Parameters
    ----------
    waldiez_flow : WaldiezFlow
        A WaldiezFlow instance.
    """
    waldiez = Waldiez(flow=waldiez_flow)
    exporter = WaldiezExporter(waldiez)
    output_file = Path("waldiez.py")
    exporter.export(output_file)
    assert output_file.exists()
    output_file.unlink()


def test_export_to_ipynb(waldiez_flow: WaldiezFlow) -> None:
    """Test exporting to Jupyter Notebook.

    Parameters
    ----------
    waldiez_flow : WaldiezFlow
        A WaldiezFlow instance.
    """
    waldiez = Waldiez(flow=waldiez_flow)
    exporter = WaldiezExporter(waldiez)
    output_file = Path("waldiez.ipynb")
    exporter.export(output_file)
    assert output_file.exists()
    output_file.unlink()


def test_export_to_waldiez(waldiez_flow: WaldiezFlow) -> None:
    """Test exporting to Waldiez file.

    Parameters
    ----------
    waldiez_flow : WaldiezFlow
        A WaldiezFlow instance.
    """
    waldiez = Waldiez(flow=waldiez_flow)
    exporter = WaldiezExporter(waldiez)
    output_file = Path("waldiez.waldiez")
    exporter.export(output_file)
    assert output_file.exists()
    output_file.unlink()


def test_export_to_invalid_extension(waldiez_flow: WaldiezFlow) -> None:
    """Test exporting to invalid extension.

    Parameters
    ----------
    waldiez_flow : WaldiezFlow
        A WaldiezFlow instance.
    """
    waldiez = Waldiez(flow=waldiez_flow)
    exporter = WaldiezExporter(waldiez)
    output_file = Path("waldiez.invalid")
    with pytest.raises(ValueError):
        exporter.export(output_file)


def test_export_complex_flow() -> None:
    """Test exporting invalid flow."""
    flow = get_flow()
    waldiez = Waldiez(flow=flow)
    exporter = WaldiezExporter(waldiez)
    output_file = Path("flow.py")
    exporter.export(output_file)
    assert output_file.exists()
    output_file.unlink()
    skill_file = Path("skill_name.py")
    assert skill_file.exists()
    skill_file.unlink()
