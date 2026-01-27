import sys
from pathlib import Path
import shutil
import pytest

if shutil.which("chromedriver") is None:
    pytest.skip("chromedriver not found; skipping Dash UI tests", allow_module_level=True)

# Ensure project root is importable when running pytest
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import app


def test_header_is_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("h1", timeout=5)
    assert dash_duo.find_element("h1").text == "Pink Morsel Sales Visualiser"


def test_visualisation_is_present(dash_duo):
    dash_duo.start_server(app)
    # dcc.Graph renders a container with the same id
    dash_duo.wait_for_element("#sales_chart", timeout=5)
    assert dash_duo.find_element("#sales_chart") is not None


def test_region_picker_is_present(dash_duo):
    dash_duo.start_server(app)
    # dcc.Dropdown renders a container div with that id
    dash_duo.wait_for_element("#region", timeout=5)
    assert dash_duo.find_element("#region") is not None
