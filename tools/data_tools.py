from __future__ import annotations

from typing import Optional

from fastmcp import FastMCP

from pbi_core import tom_backend
from pbi_core.state import get_state


def _require_session() -> Optional[dict]:
    if get_state().session is None:
        return {"status": "error", "message": "No active session — call pbi_connect first"}
    return None


def _w(r):
    return {"items": r, "count": len(r)} if isinstance(r, list) else r


# ---------------------------------------------------------------------------
# Partition tools
# ---------------------------------------------------------------------------


def _partition_list(table: str) -> dict:
    """List partitions in a table."""
    err = _require_session()
    if err:
        return err
    return _w(tom_backend.partition_list(get_state().session.model, table_name=table))


def _partition_get(table: str, name: str) -> dict:
    """Get details of a specific partition."""
    err = _require_session()
    if err:
        return err
    try:
        model = get_state().session.model
        # Get partition via backend helpers
        table_obj = None
        for t in model.Tables:
            if t.Name == table:
                table_obj = t
                break
        if table_obj is None:
            return {"status": "error", "message": f"Table '{table}' not found"}
        for p in table_obj.Partitions:
            if p.Name == name:
                return {
                    "name": str(p.Name),
                    "tableName": table,
                    "mode": str(p.Mode),
                    "sourceType": str(p.SourceType),
                    "state": str(p.State),
                }
        return {"status": "error", "message": f"Partition '{name}' not found in table '{table}'"}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


def _partition_update(table: str, name: str, expression: Optional[str] = None, mode: Optional[str] = None) -> dict:
    """Update partition expression or mode (stub — use partition_create/delete for full control)."""
    err = _require_session()
    if err:
        return err
    return {
        "status": "not_implemented",
        "message": "partition_update is not yet available; use pbi_partition_list and pbi_database_import_tmdl to manage partitions",
    }


# ---------------------------------------------------------------------------
# Named expression tools
# ---------------------------------------------------------------------------


def _expression_get(name: str) -> dict:
    """Get a named expression (shared expression / M parameter)."""
    err = _require_session()
    if err:
        return err
    return tom_backend.expression_get(get_state().session.model, name=name)


def _expression_list() -> dict:
    """List all named expressions."""
    err = _require_session()
    if err:
        return err
    return _w(tom_backend.expression_list(get_state().session.model))


# ---------------------------------------------------------------------------
# Calendar / culture tools
# ---------------------------------------------------------------------------


def _calendar_list() -> dict:
    """List cultures defined in the model."""
    err = _require_session()
    if err:
        return err
    return _w(tom_backend.culture_list(get_state().session.model))


def _calendar_define(name: str) -> dict:
    """Create a culture entry (used for calendar localisation)."""
    err = _require_session()
    if err:
        return err
    return tom_backend.culture_create(get_state().session.model, name=name)


def _culture_set(name: str) -> dict:
    """Set the model culture (create if it doesn't exist)."""
    err = _require_session()
    if err:
        return err
    model = get_state().session.model
    # Update the model-level culture property
    try:
        model.Culture = name
        model.SaveChanges()
        return {"status": "updated", "culture": name}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


def _model_stats() -> dict:
    """Return model statistics: table, column, measure, relationship counts."""
    err = _require_session()
    if err:
        return err
    return tom_backend.model_get_stats(get_state().session.model)


def register_tools(mcp: FastMCP) -> None:
    for fn in (
        _partition_list,
        _partition_get,
        _partition_update,
        _expression_get,
        _expression_list,
        _calendar_list,
        _calendar_define,
        _culture_set,
        _model_stats,
    ):
        mcp.tool(name="pbi_" + fn.__name__.lstrip("_"))(fn)
