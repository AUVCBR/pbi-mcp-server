from __future__ import annotations

from dataclasses import asdict
from typing import Optional

from fastmcp import FastMCP

from pbi_core import dotnet_loader, session as session_module
from pbi_core.connection_store import load_connections, get_active_connection
from pbi_core.platform import discover_pbi_port, discover_pbip_path
from pbi_core.state import get_state


def _connect(
    data_source: Optional[str] = None,
    catalog: Optional[str] = None,
    report_path: Optional[str] = None,
    name: Optional[str] = None,
) -> dict:
    state = get_state()
    if data_source is None:
        port = discover_pbi_port()
        if port is None:
            return {
                "status": "error",
                "message": "Power BI Desktop not found. Open a .pbip file in Desktop first.",
            }
        data_source = f"localhost:{port}"
    dotnet_loader._ensure_initialized()
    sess = session_module.connect(data_source, catalog or "")
    state.session = sess
    if report_path:
        state.report_path = report_path
    elif state.report_path is None:
        state.report_path = discover_pbip_path()
    # Session has data_source field; catalog lives in sess.database.Name if connected
    db_name = None
    try:
        db_name = str(sess.database.Name) if sess.database is not None else None
    except Exception:
        pass
    return {
        "status": "connected",
        "data_source": data_source,
        "catalog": db_name or catalog,
        "report_path": state.report_path,
        "report_path_auto_detected": report_path is None and state.report_path is not None,
    }


def _disconnect() -> dict:
    state = get_state()
    if state.session is None:
        return {"status": "not_connected"}
    session_module.disconnect(state.session)
    state.session = None
    return {"status": "disconnected"}


def _connection_status() -> dict:
    state = get_state()
    return {
        "connected": state.session is not None,
        "report_path": state.report_path,
    }


def _connections_list() -> dict:
    store = load_connections()
    # store.connections is a dict[str, ConnectionInfo]
    return {"connections": [asdict(c) for c in store.connections.values()]}


def _connections_last() -> dict:
    store = load_connections()
    last = get_active_connection(store)
    if last is None:
        return {"status": "no_connections"}
    return {"connection": asdict(last)}


def register_tools(mcp: FastMCP) -> None:
    for fn in (_connect, _disconnect, _connection_status, _connections_list, _connections_last):
        mcp.tool(name="pbi_" + fn.__name__.lstrip("_"))(fn)
