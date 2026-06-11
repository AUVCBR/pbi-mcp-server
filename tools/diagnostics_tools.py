from __future__ import annotations

from typing import Optional

from fastmcp import FastMCP

from pbi_core import tom_backend
from pbi_core.state import get_state


def _require_session() -> Optional[dict]:
    if get_state().session is None:
        return {"status": "error", "message": "No active session — call pbi_connect first"}
    return None


def _trace_start() -> dict:
    """Start a diagnostic trace on the server."""
    err = _require_session()
    if err:
        return err
    try:
        return tom_backend.trace_start(get_state().session.server)
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


def _trace_stop() -> dict:
    """Stop the active diagnostic trace."""
    err = _require_session()
    if err:
        return err
    try:
        return tom_backend.trace_stop()
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


def _trace_fetch() -> dict:
    """Fetch collected trace events."""
    err = _require_session()
    if err:
        return err
    events = tom_backend.trace_fetch()
    return {"events": events, "count": len(events)}


def _trace_export(path: str) -> dict:
    """Export trace events to a JSON file."""
    err = _require_session()
    if err:
        return err
    try:
        return tom_backend.trace_export(path=path)
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


def register_tools(mcp: FastMCP) -> None:
    for fn in (
        _trace_start,
        _trace_stop,
        _trace_fetch,
        _trace_export,
    ):
        mcp.tool(name="pbi_" + fn.__name__.lstrip("_"))(fn)
