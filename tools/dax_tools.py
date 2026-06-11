from __future__ import annotations

from typing import Optional

from fastmcp import FastMCP

from pbi_core import adomd_backend
from pbi_core.state import get_state


def _require_session() -> Optional[dict]:
    if get_state().session is None:
        return {"status": "error", "message": "No active session — call pbi_connect first"}
    return None


def _dax_execute(query: str, max_rows: Optional[int] = None, timeout: int = 200) -> dict:
    """Execute a DAX query and return results."""
    err = _require_session()
    if err:
        return err
    return adomd_backend.execute_dax(
        get_state().session.adomd_connection,
        query=query,
        max_rows=max_rows,
        timeout=timeout,
    )


def _dax_validate(query: str, timeout: int = 10) -> dict:
    """Validate a DAX query without returning data."""
    err = _require_session()
    if err:
        return err
    return adomd_backend.validate_dax(
        get_state().session.adomd_connection,
        query=query,
        timeout=timeout,
    )


def _dax_clear_cache(database_id: str = "") -> dict:
    """Clear the Analysis Services cache."""
    err = _require_session()
    if err:
        return err
    return adomd_backend.clear_cache(
        get_state().session.adomd_connection,
        database_id=database_id,
    )


def register_tools(mcp: FastMCP) -> None:
    for fn in (_dax_execute, _dax_validate, _dax_clear_cache):
        mcp.tool(name="pbi_" + fn.__name__.lstrip("_"))(fn)
