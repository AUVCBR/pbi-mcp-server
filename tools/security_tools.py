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
# Security role tools  (backend uses role_* not security_role_*)
# ---------------------------------------------------------------------------


def _security_role_list() -> dict:
    """List all security roles in the model."""
    err = _require_session()
    if err:
        return err
    return _w(tom_backend.role_list(get_state().session.model))


def _security_role_get(name: str) -> dict:
    """Get details of a security role including its table filters."""
    err = _require_session()
    if err:
        return err
    return tom_backend.role_get(get_state().session.model, name=name)


def _security_role_create(name: str, description: Optional[str] = None) -> dict:
    """Create a new security role."""
    err = _require_session()
    if err:
        return err
    return tom_backend.role_create(
        get_state().session.model, name=name, description=description
    )


def _security_role_delete(name: str) -> dict:
    """Delete a security role."""
    err = _require_session()
    if err:
        return err
    return tom_backend.role_delete(get_state().session.model, name=name)


def _security_role_add_filter(role: str, table: str, filter_expression: str) -> dict:
    """Add or update a row-level security filter on a table for a role.

    Note: This operation requires direct TOM manipulation.
    """
    err = _require_session()
    if err:
        return err
    try:
        model = get_state().session.model
        # Locate the role
        role_obj = None
        for r in model.Roles:
            if r.Name == role:
                role_obj = r
                break
        if role_obj is None:
            return {"status": "error", "message": f"Role '{role}' not found"}

        # Find or create the table permission
        tp_obj = None
        for tp in role_obj.TablePermissions:
            if tp.Table.Name == table:
                tp_obj = tp
                break

        if tp_obj is None:
            # Need to create a new TablePermission — requires .NET interop
            return {
                "status": "not_implemented",
                "message": "Creating new table permissions requires .NET interop (run against a live model)",
            }

        tp_obj.FilterExpression = filter_expression
        model.SaveChanges()
        return {"status": "updated", "role": role, "table": table, "filter": filter_expression}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


# ---------------------------------------------------------------------------
# Perspective tools
# ---------------------------------------------------------------------------


def _perspective_list() -> dict:
    """List all perspectives in the model."""
    err = _require_session()
    if err:
        return err
    return _w(tom_backend.perspective_list(get_state().session.model))


def _perspective_create(name: str, description: Optional[str] = None) -> dict:
    """Create a new perspective."""
    err = _require_session()
    if err:
        return err
    return tom_backend.perspective_create(
        get_state().session.model, name=name, description=description
    )


def _perspective_delete(name: str) -> dict:
    """Delete a perspective."""
    err = _require_session()
    if err:
        return err
    return tom_backend.perspective_delete(get_state().session.model, name=name)


def register_tools(mcp: FastMCP) -> None:
    for fn in (
        _security_role_list,
        _security_role_get,
        _security_role_create,
        _security_role_delete,
        _security_role_add_filter,
        _perspective_list,
        _perspective_create,
        _perspective_delete,
    ):
        mcp.tool(name="pbi_" + fn.__name__.lstrip("_"))(fn)
