from unittest.mock import patch
from pathlib import Path
from tools.visual_tools import _visual_list, _visual_add, _visual_delete, _visual_bind, _visual_types
from pbi_core.state import get_state, reset_state

REPORT_PATH = "C:/Sales.Report/definition"


def setup_function():
    reset_state()


def test_visual_types_returns_list():
    result = _visual_types()
    assert "visual_types" in result
    assert isinstance(result["visual_types"], list)
    assert len(result["visual_types"]) > 0


def test_visual_list():
    mock_visuals = [{"name": "v1", "visualType": "barChart"}]
    with patch("tools.visual_tools.visual_backend.visual_list", return_value=mock_visuals) as m:
        result = _visual_list(page_name="Overview", report_path=REPORT_PATH)
    assert result == mock_visuals


def test_visual_add():
    mock_result = {"status": "created", "name": "abc123", "visual_type": "barChart"}
    with patch("tools.visual_tools.visual_backend.visual_add", return_value=mock_result):
        result = _visual_add(
            page_name="Overview",
            visual_type="barChart",
            x=100,
            y=50,
            width=400,
            height=300,
            report_path=REPORT_PATH,
        )
    assert result["status"] == "created"


def test_visual_delete():
    mock_result = {"status": "deleted", "name": "abc123"}
    with patch("tools.visual_tools.visual_backend.visual_delete", return_value=mock_result):
        result = _visual_delete(page_name="Overview", visual_name="abc123", report_path=REPORT_PATH)
    assert result["status"] == "deleted"


def test_visual_bind():
    mock_result = {"status": "bound", "name": "abc123"}
    with patch("tools.visual_tools.visual_backend.visual_bind", return_value=mock_result):
        result = _visual_bind(
            page_name="Overview",
            visual_name="abc123",
            role="Category",
            table="Sales",
            column="Region",
            report_path=REPORT_PATH,
        )
    assert result["status"] == "bound"


def test_visual_no_path_error():
    result = _visual_list(page_name="Overview")
    assert result["status"] == "error"
