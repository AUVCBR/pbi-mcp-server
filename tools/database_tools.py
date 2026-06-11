from __future__ import annotations

from typing import Optional

from fastmcp import FastMCP

from pbi_core import tom_backend
from pbi_core.state import get_state

try:
    from pbi_core import tmdl_diff as _tmdl_diff
    _TMDL_DIFF_AVAILABLE = True
except ImportError:
    _TMDL_DIFF_AVAILABLE = False


def _require_session() -> Optional[dict]:
    if get_state().session is None:
        return {"status": "error", "message": "No active session — call pbi_connect first"}
    return None


def _w(r):
    return {"items": r, "count": len(r)} if isinstance(r, list) else r


def _database_list() -> dict:
    """List all databases on the connected server."""
    err = _require_session()
    if err:
        return err
    return _w(tom_backend.database_list(get_state().session.server))


def _database_export_tmdl(folder_path: str) -> dict:
    """Export the current database to a TMDL folder."""
    err = _require_session()
    if err:
        return err
    return tom_backend.export_tmdl(get_state().session.database, folder_path=folder_path)


def _database_import_tmdl(folder_path: str) -> dict:
    """Import a model from a TMDL folder into the current database."""
    err = _require_session()
    if err:
        return err
    return tom_backend.import_tmdl(get_state().session.server, folder_path=folder_path)


def _database_export_tmsl() -> dict:
    """Export the current database as a TMSL (JSON) script."""
    err = _require_session()
    if err:
        return err
    return tom_backend.export_tmsl(get_state().session.database)


def _database_diff_tmdl(base_folder: str, head_folder: str) -> dict:
    """Compare two TMDL export folders and return a structured diff."""
    if not _TMDL_DIFF_AVAILABLE:
        return {"status": "not_implemented", "message": "tmdl_diff module not available"}
    try:
        from pbi_core.tmdl_diff import diff_tmdl_folders
        return diff_tmdl_folders(base_folder, head_folder)
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


def _transaction_begin() -> dict:
    """Begin an explicit transaction on the server."""
    err = _require_session()
    if err:
        return err
    return tom_backend.transaction_begin(get_state().session.server)


def _transaction_commit(transaction_id: str = "") -> dict:
    """Commit the active or specified transaction."""
    err = _require_session()
    if err:
        return err
    return tom_backend.transaction_commit(get_state().session.server, transaction_id=transaction_id)


def _transaction_rollback(transaction_id: str = "") -> dict:
    """Rollback the active or specified transaction."""
    err = _require_session()
    if err:
        return err
    return tom_backend.transaction_rollback(get_state().session.server, transaction_id=transaction_id)


def register_tools(mcp: FastMCP) -> None:
    for fn in (
        _database_list,
        _database_export_tmdl,
        _database_import_tmdl,
        _database_export_tmsl,
        _database_diff_tmdl,
        _transaction_begin,
        _transaction_commit,
        _transaction_rollback,
    ):
        mcp.tool(name="pbi_" + fn.__name__.lstrip("_"))(fn)
