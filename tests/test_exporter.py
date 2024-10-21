"""Test WaldieExporter."""

from pathlib import Path

from waldiez import Waldie, WaldieExporter
from waldiez.models import WaldieFlow


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
