from __future__ import annotations
from pathlib import Path
from typing import Optional
from fastmcp import FastMCP
from pbi_core import visual_backend, bulk_backend
from pbi_core.state import get_state

_TEMPLATES_DIR = Path(__file__).parent.parent / "templates" / "visuals"


def _resolve_path(report_path: Optional[str]) -> Optional[str]:
    return report_path or get_state().report_path


def _no_path_error() -> dict:
    return {
        "status": "error",
        "message": "report_path required — pass it or call pbi_connect with report_path first",
    }


def _w(r):
    return {"items": r, "count": len(r)} if isinstance(r, list) else r


def _visual_types() -> dict:
    types = sorted(p.stem for p in _TEMPLATES_DIR.glob("*.json"))
    return {"visual_types": types, "count": len(types)}


def _visual_list(page_name: str, report_path: Optional[str] = None) -> list | dict:
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return _w(visual_backend.visual_list(Path(path), page_name))


def _visual_get(page_name: str, visual_name: str, report_path: Optional[str] = None) -> dict:
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return visual_backend.visual_get(Path(path), page_name, visual_name)


def _visual_add(
    page_name: str,
    visual_type: str,
    x: int = 0,
    y: int = 0,
    width: int = 400,
    height: int = 300,
    name: Optional[str] = None,
    report_path: Optional[str] = None,
) -> dict:
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return visual_backend.visual_add(
        Path(path),
        page_name,
        visual_type=visual_type,
        x=x,
        y=y,
        width=width,
        height=height,
        name=name,
    )


def _visual_update(
    page_name: str,
    visual_name: str,
    x: Optional[int] = None,
    y: Optional[int] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    hidden: Optional[bool] = None,
    report_path: Optional[str] = None,
) -> dict:
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return visual_backend.visual_update(
        Path(path), page_name, visual_name, x=x, y=y, width=width, height=height, hidden=hidden
    )


def _visual_delete(
    page_name: str,
    visual_name: str,
    report_path: Optional[str] = None,
) -> dict:
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return visual_backend.visual_delete(Path(path), page_name, visual_name)


def _visual_bind(
    page_name: str,
    visual_name: str,
    role: str,
    table: str,
    column: str,
    is_measure: bool = False,
    report_path: Optional[str] = None,
) -> dict:
    """Bind a single field to a visual data role.

    Internally delegates to visual_backend.visual_bind which takes a bindings list.
    """
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    bindings = [{"role": role, "field": f"{table}[{column}]", "measure": is_measure}]
    return visual_backend.visual_bind(Path(path), page_name, visual_name, bindings)


def _visual_bind_many(
    page_name: str,
    visual_name: str,
    bindings: list,
    report_path: Optional[str] = None,
) -> dict:
    """Bind multiple fields at once using the bindings list format.

    Each binding: {"role": str, "field": "Table[Column]", "measure": bool (optional)}
    """
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return visual_backend.visual_bind(Path(path), page_name, visual_name, bindings)


def _visual_bulk_update(
    page_name: str,
    where_type: Optional[str] = None,
    where_name_pattern: Optional[str] = None,
    set_hidden: Optional[bool] = None,
    set_width: Optional[float] = None,
    set_height: Optional[float] = None,
    set_x: Optional[float] = None,
    set_y: Optional[float] = None,
    report_path: Optional[str] = None,
) -> dict:
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return bulk_backend.visual_bulk_update(
        Path(path),
        page_name,
        where_type=where_type,
        where_name_pattern=where_name_pattern,
        set_hidden=set_hidden,
        set_width=set_width,
        set_height=set_height,
        set_x=set_x,
        set_y=set_y,
    )


def _visual_bulk_delete(
    page_name: str,
    where_type: Optional[str] = None,
    where_name_pattern: Optional[str] = None,
    report_path: Optional[str] = None,
) -> dict:
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return bulk_backend.visual_bulk_delete(
        Path(path), page_name, where_type=where_type, where_name_pattern=where_name_pattern
    )


def _visual_bulk_bind(
    page_name: str,
    visual_type: str,
    bindings: list,
    name_pattern: Optional[str] = None,
    report_path: Optional[str] = None,
) -> dict:
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return bulk_backend.visual_bulk_bind(
        Path(path), page_name, visual_type=visual_type, bindings=bindings, name_pattern=name_pattern
    )


def _visual_where(
    page_name: str,
    visual_type: Optional[str] = None,
    name_pattern: Optional[str] = None,
    x_min: Optional[float] = None,
    x_max: Optional[float] = None,
    y_min: Optional[float] = None,
    y_max: Optional[float] = None,
    report_path: Optional[str] = None,
) -> list | dict:
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return bulk_backend.visual_where(
        Path(path),
        page_name,
        visual_type=visual_type,
        name_pattern=name_pattern,
        x_min=x_min,
        x_max=x_max,
        y_min=y_min,
        y_max=y_max,
    )


def register_tools(mcp: FastMCP) -> None:
    for fn in (
        _visual_types,
        _visual_list,
        _visual_get,
        _visual_add,
        _visual_update,
        _visual_delete,
        _visual_bind,
        _visual_bind_many,
        _visual_bulk_update,
        _visual_bulk_delete,
        _visual_bulk_bind,
        _visual_where,
    ):
        mcp.tool(name="pbi_" + fn.__name__.lstrip("_"))(fn)
