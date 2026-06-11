from unittest.mock import patch
from tools.page_tools import _page_list, _page_add, _page_delete
from pbi_core.state import get_state, reset_state

REPORT_PATH = "C:/Sales.Report/definition"


def setup_function():
    reset_state()


def test_page_list_explicit_path():
    mock_pages = [{"name": "p1", "displayName": "Overview"}]
    with patch("tools.page_tools.report_backend.page_list", return_value=mock_pages) as m:
        result = _page_list(report_path=REPORT_PATH)
    m.assert_called_once()
    assert result == mock_pages


def test_page_list_uses_state_path():
    get_state().report_path = REPORT_PATH
    mock_pages = [{"name": "p1", "displayName": "Overview"}]
    with patch("tools.page_tools.report_backend.page_list", return_value=mock_pages):
        result = _page_list()
    assert result == mock_pages


def test_page_list_no_path_error():
    result = _page_list()
    assert result["status"] == "error"
    assert "report_path" in result["message"]


def test_page_add():
    mock_result = {"status": "created", "name": "p_new"}
    with patch("tools.page_tools.report_backend.page_add", return_value=mock_result):
        result = _page_add(display_name="New Page", report_path=REPORT_PATH)
    assert result["status"] == "created"


def test_page_delete():
    mock_result = {"status": "deleted", "name": "p1"}
    with patch("tools.page_tools.report_backend.page_delete", return_value=mock_result):
        result = _page_delete(page_name="p1", report_path=REPORT_PATH)
    assert result["status"] == "deleted"
