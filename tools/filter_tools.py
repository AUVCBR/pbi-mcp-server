from __future__ import annotations
from pathlib import Path
from typing import Optional
from fastmcp import FastMCP
from pbi_core import filter_backend
from pbi_core.state import get_state


def _resolve_path(p: Optional[str]) -> Optional[str]:
    return p or get_state().report_path


def _no_path_error() -> dict:
    return {"status": "error", "message": "report_path required"}


def _w(r):
    return {"items": r, "count": len(r)} if isinstance(r, list) else r


def _filters_list(
    page_name: str,
    visual_name: Optional[str] = None,
    report_path: Optional[str] = None,
) -> list | dict:
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return _w(filter_backend.filter_list(Path(path), page_name, visual_name=visual_name))


def _filters_add_categorical(
    page_name: str,
    table: str,
    column: str,
    values: list,
    visual_name: Optional[str] = None,
    report_path: Optional[str] = None,
) -> dict:
    """Add a categorical filter. Specify table and column separately."""
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return filter_backend.filter_add_categorical(
        Path(path), page_name, table=table, column=column, values=values, visual_name=visual_name
    )


def _filters_add_topn(
    page_name: str,
    table: str,
    column: str,
    n: int,
    order_by_table: str,
    order_by_column: str,
    direction: str = "Top",
    visual_name: Optional[str] = None,
    report_path: Optional[str] = None,
) -> dict:
    """Add a TopN filter. Requires the table/column to filter and the order-by table/column."""
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return filter_backend.filter_add_topn(
        Path(path),
        page_name,
        table=table,
        column=column,
        n=n,
        order_by_table=order_by_table,
        order_by_column=order_by_column,
        direction=direction,
        visual_name=visual_name,
    )


def _filters_add_relative_date(
    page_name: str,
    table: str,
    column: str,
    amount: int,
    time_unit: str,
    visual_name: Optional[str] = None,
    report_path: Optional[str] = None,
) -> dict:
    """Add a relative date filter. time_unit: days/weeks/months/years."""
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return filter_backend.filter_add_relative_date(
        Path(path),
        page_name,
        table=table,
        column=column,
        amount=amount,
        time_unit=time_unit,
        visual_name=visual_name,
    )


def _filters_remove(
    page_name: str,
    filter_name: str,
    visual_name: Optional[str] = None,
    report_path: Optional[str] = None,
) -> dict:
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return filter_backend.filter_remove(Path(path), page_name, filter_name, visual_name=visual_name)


def _filters_clear(
    page_name: str,
    visual_name: Optional[str] = None,
    report_path: Optional[str] = None,
) -> dict:
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return filter_backend.filter_clear(Path(path), page_name, visual_name=visual_name)


def register_tools(mcp: FastMCP) -> None:
    for fn in (
        _filters_list,
        _filters_add_categorical,
        _filters_add_topn,
        _filters_add_relative_date,
        _filters_remove,
        _filters_clear,
    ):
        mcp.tool(name="pbi_" + fn.__name__.lstrip("_"))(fn)
