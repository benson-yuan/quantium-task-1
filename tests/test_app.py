import pytest
import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Import the Dash app from your app.py
from app import app


def test_layout_has_header():
    """App should have a clear title header."""
    # layout is an html.Div; children include H1
    layout = app.layout
    text = str(layout)
    assert "Pink Morsel Sales Visualiser" in text


def test_layout_has_dropdown_and_graph_ids():
    """Critical components must exist with correct IDs."""
    layout = app.layout
    text = str(layout)

    # These IDs must match your Dash component IDs
    assert "id='view'" in text or 'id="view"' in text
    assert "id='sales_chart'" in text or 'id="sales_chart"' in text
    assert "id='answer'" in text or 'id="answer"' in text


@pytest.mark.parametrize("view_value", ["total", "by_region"])
def test_callback_runs_without_error(view_value):
    """
    The callback logic should execute and return a Plotly figure + answer string.
    This avoids full browser tests but still validates behaviour.
    """
    # Access the callback function directly by importing it if you expose it,
    # OR (simpler) call the function attribute if it's in module scope.
    # If your callback function is named update_chart in app.py, import it:
    from app import update_chart

    fig, answer = update_chart(view_value, "ALL")

    # Figure should have data traces
    assert fig is not None
    assert hasattr(fig, "data")
    assert len(fig.data) >= 1

    # Answer should be a string and non-empty
    assert isinstance(answer, str)
    assert len(answer) > 0
