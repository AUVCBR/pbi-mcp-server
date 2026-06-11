from unittest.mock import patch, MagicMock
from tools.model_tools import _measure_list, _measure_create, _measure_delete
from pbi_core.state import get_state


def test_measure_list_no_session():
    result = _measure_list()
    assert result["status"] == "error"
    assert "pbi_connect" in result["message"]


def test_measure_list_with_session():
    get_state().session = MagicMock()
    mock_measures = [{"name": "Revenue", "table": "Sales"}]
    with patch("tools.model_tools.tom_backend.measure_list", return_value=mock_measures):
        result = _measure_list()
    assert result == mock_measures


def test_measure_create_no_session():
    result = _measure_create(table="Sales", name="Revenue", expression="SUM(Sales[Revenue])")
    assert result["status"] == "error"


def test_measure_delete_no_session():
    result = _measure_delete(table="Sales", name="Revenue")
    assert result["status"] == "error"
