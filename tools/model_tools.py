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
# Measure tools
# ---------------------------------------------------------------------------


def _measure_list(table: Optional[str] = None) -> dict:
    err = _require_session()
    if err:
        return err
    return _w(tom_backend.measure_list(get_state().session.model, table_name=table))


def _measure_get(table: str, name: str) -> dict:
    err = _require_session()
    if err:
        return err
    return tom_backend.measure_get(get_state().session.model, table_name=table, measure_name=name)


def _measure_create(
    table: str,
    name: str,
    expression: str,
    format_string: Optional[str] = None,
    description: Optional[str] = None,
    display_folder: Optional[str] = None,
    is_hidden: bool = False,
) -> dict:
    err = _require_session()
    if err:
        return err
    return tom_backend.measure_create(
        get_state().session.model,
        table_name=table,
        name=name,
        expression=expression,
        format_string=format_string,
        description=description,
        display_folder=display_folder,
        is_hidden=is_hidden,
    )


def _measure_update(
    table: str,
    name: str,
    expression: Optional[str] = None,
    format_string: Optional[str] = None,
    description: Optional[str] = None,
    display_folder: Optional[str] = None,
) -> dict:
    err = _require_session()
    if err:
        return err
    return tom_backend.measure_update(
        get_state().session.model,
        table_name=table,
        name=name,
        expression=expression,
        format_string=format_string,
        description=description,
        display_folder=display_folder,
    )


def _measure_delete(table: str, name: str) -> dict:
    err = _require_session()
    if err:
        return err
    return tom_backend.measure_delete(
        get_state().session.model, table_name=table, name=name
    )


# ---------------------------------------------------------------------------
# Table tools
# ---------------------------------------------------------------------------


def _table_list() -> dict:
    err = _require_session()
    if err:
        return err
    return _w(tom_backend.table_list(get_state().session.model))


def _table_get(name: str) -> dict:
    err = _require_session()
    if err:
        return err
    return tom_backend.table_get(get_state().session.model, table_name=name)


# ---------------------------------------------------------------------------
# Column tools
# ---------------------------------------------------------------------------


def _column_list(table: str) -> dict:
    err = _require_session()
    if err:
        return err
    return _w(tom_backend.column_list(get_state().session.model, table_name=table))


# ---------------------------------------------------------------------------
# Relationship tools
# ---------------------------------------------------------------------------


def _relationship_list() -> dict:
    err = _require_session()
    if err:
        return err
    return _w(tom_backend.relationship_list(get_state().session.model))


def _relationship_create(
    from_table: str,
    from_column: str,
    to_table: str,
    to_column: str,
    name: Optional[str] = None,
    cross_filter: str = "OneDirection",
    is_active: bool = True,
) -> dict:
    err = _require_session()
    if err:
        return err
    return tom_backend.relationship_create(
        get_state().session.model,
        from_table=from_table,
        from_column=from_column,
        to_table=to_table,
        to_column=to_column,
        name=name,
        cross_filter=cross_filter,
        is_active=is_active,
    )


# ---------------------------------------------------------------------------
# Hierarchy tools
# ---------------------------------------------------------------------------


def _hierarchy_list(table: Optional[str] = None) -> dict:
    err = _require_session()
    if err:
        return err
    return _w(tom_backend.hierarchy_list(get_state().session.model, table_name=table))


def _hierarchy_create(
    table: str,
    name: str,
    description: Optional[str] = None,
) -> dict:
    err = _require_session()
    if err:
        return err
    return tom_backend.hierarchy_create(
        get_state().session.model,
        table_name=table,
        name=name,
        description=description,
    )


def _hierarchy_delete(table: str, name: str) -> dict:
    err = _require_session()
    if err:
        return err
    return tom_backend.hierarchy_delete(
        get_state().session.model, table_name=table, name=name
    )


# ---------------------------------------------------------------------------
# Calculation group tools
# ---------------------------------------------------------------------------


def _calc_group_list() -> dict:
    err = _require_session()
    if err:
        return err
    return _w(tom_backend.calc_group_list(get_state().session.model))


def _calc_group_create(
    name: str,
    description: Optional[str] = None,
    precedence: Optional[int] = None,
) -> dict:
    err = _require_session()
    if err:
        return err
    return tom_backend.calc_group_create(
        get_state().session.model,
        name=name,
        description=description,
        precedence=precedence,
    )


def _calc_group_delete(name: str) -> dict:
    err = _require_session()
    if err:
        return err
    return tom_backend.calc_group_delete(get_state().session.model, name=name)


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


def register_tools(mcp: FastMCP) -> None:
    for fn in (
        _measure_list,
        _measure_get,
        _measure_create,
        _measure_update,
        _measure_delete,
        _table_list,
        _table_get,
        _column_list,
        _relationship_list,
        _relationship_create,
        _hierarchy_list,
        _hierarchy_create,
        _hierarchy_delete,
        _calc_group_list,
        _calc_group_create,
        _calc_group_delete,
    ):
        mcp.tool(name="pbi_" + fn.__name__.lstrip("_"))(fn)
