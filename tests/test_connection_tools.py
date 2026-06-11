from unittest.mock import MagicMock, patch
from tools.connection_tools import (
    _connect, _disconnect, _connection_status, _connections_list, _connections_last
)
from pbi_core.state import get_state


def test_connect_no_desktop_running():
    with patch("tools.connection_tools.discover_pbi_port", return_value=None):
        result = _connect()
    assert result["status"] == "error"
    assert "Power BI Desktop not found" in result["message"]


def test_connect_sets_session_and_path():
    mock_sess = MagicMock()
    # Session.database.Name is used for connection_name; data_source is on the session
    mock_sess.data_source = "localhost:54321"
    with (
        patch("tools.connection_tools.discover_pbi_port", return_value=54321),
        patch("tools.connection_tools.dotnet_loader._ensure_initialized"),
        patch("tools.connection_tools.session_module.connect", return_value=mock_sess),
    ):
        result = _connect(report_path="C:/Sales.pbip")
    assert result["status"] == "connected"
    assert result["data_source"] == "localhost:54321"
    assert get_state().session is mock_sess
    assert get_state().report_path == "C:/Sales.pbip"


def test_disconnect_when_not_connected():
    result = _disconnect()
    assert result["status"] == "not_connected"


def test_disconnect_clears_session():
    mock_sess = MagicMock()
    get_state().session = mock_sess
    with patch("tools.connection_tools.session_module.disconnect") as mock_disc:
        result = _disconnect()
    mock_disc.assert_called_once_with(mock_sess)
    assert result["status"] == "disconnected"
    assert get_state().session is None


def test_status_not_connected():
    result = _connection_status()
    assert result["connected"] is False


def test_status_connected():
    get_state().session = MagicMock()
    get_state().report_path = "C:/Sales.pbip"
    result = _connection_status()
    assert result["connected"] is True
    assert result["report_path"] == "C:/Sales.pbip"


def test_connections_list_empty():
    from pbi_core.connection_store import ConnectionStore
    with patch("tools.connection_tools.load_connections", return_value=ConnectionStore()):
        result = _connections_list()
    assert result["connections"] == []


def test_connections_last_none():
    from pbi_core.connection_store import ConnectionStore
    with patch("tools.connection_tools.load_connections", return_value=ConnectionStore()):
        result = _connections_last()
    assert result["status"] == "no_connections"
