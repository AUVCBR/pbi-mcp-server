from __future__ import annotations
from pathlib import Path
from typing import Optional
from fastmcp import FastMCP
from pbi_core import format_backend
from pbi_core.state import get_state


def _resolve_path(p: Optional[str]) -> Optional[str]:
    return p or get_state().report_path


def _no_path_error() -> dict:
    return {"status": "error", "message": "report_path required"}


def _format_get(page_name: str, visual_name: str, report_path: Optional[str] = None) -> dict:
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return format_backend.format_get(Path(path), page_name, visual_name)


def _format_clear(page_name: str, visual_name: str, report_path: Optional[str] = None) -> dict:
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return format_backend.format_clear(Path(path), page_name, visual_name)


def _format_background_gradient(
    page_name: str,
    visual_name: str,
    input_table: str,
    input_column: str,
    field_query_ref: str,
    min_color: str = "#FFFFFF",
    max_color: str = "#118DFF",
    report_path: Optional[str] = None,
) -> dict:
    """Add a linear gradient background color rule to a visual column.

    input_table/input_column: the measure/column driving the gradient.
    field_query_ref: the queryRef of the target field (e.g. 'Sum(financials.Profit)').
    min_color/max_color: hex colors for the gradient endpoints.
    """
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return format_backend.format_background_gradient(
        Path(path),
        page_name,
        visual_name,
        input_table=input_table,
        input_column=input_column,
        field_query_ref=field_query_ref,
        min_color=min_color,
        max_color=max_color,
    )


def _format_background_conditional(
    page_name: str,
    visual_name: str,
    input_table: str,
    input_column: str,
    threshold: float,
    color_hex: str,
    comparison: str = "gt",
    field_query_ref: Optional[str] = None,
    report_path: Optional[str] = None,
) -> dict:
    """Add a rule-based conditional background color to a visual column.

    comparison: eq/neq/gt/gte/lt/lte (default gt).
    field_query_ref: selector.metadata queryRef — defaults to 'Sum(table.column)'.
    """
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return format_backend.format_background_conditional(
        Path(path),
        page_name,
        visual_name,
        input_table=input_table,
        input_column=input_column,
        threshold=threshold,
        color_hex=color_hex,
        comparison=comparison,
        field_query_ref=field_query_ref,
    )


def _format_background_measure(
    page_name: str,
    visual_name: str,
    measure_table: str,
    measure_property: str,
    field_query_ref: str,
    report_path: Optional[str] = None,
) -> dict:
    """Add a measure-driven background color rule to a visual column.

    measure_table/measure_property: the DAX measure that returns a hex color string.
    field_query_ref: the queryRef of the target field.
    """
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return format_backend.format_background_measure(
        Path(path),
        page_name,
        visual_name,
        measure_table=measure_table,
        measure_property=measure_property,
        field_query_ref=field_query_ref,
    )


def register_tools(mcp: FastMCP) -> None:
    for fn in (
        _format_get,
        _format_clear,
        _format_background_gradient,
        _format_background_conditional,
        _format_background_measure,
    ):
        mcp.tool(name="pbi_" + fn.__name__.lstrip("_"))(fn)
