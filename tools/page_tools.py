from __future__ import annotations
from pathlib import Path
from typing import Optional
from fastmcp import FastMCP
from pbi_core import report_backend
from pbi_core.state import get_state


def _resolve_path(report_path: Optional[str]) -> Optional[str]:
    return report_path or get_state().report_path


def _no_path_error() -> dict:
    return {
        "status": "error",
        "message": "report_path required — pass it or call pbi_connect with report_path first",
    }


def _page_list(report_path: Optional[str] = None) -> list | dict:
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return report_backend.page_list(Path(path))


def _page_get(page_name: str, report_path: Optional[str] = None) -> dict:
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return report_backend.page_get(Path(path), page_name)


def _page_add(
    display_name: str,
    name: Optional[str] = None,
    width: int = 1280,
    height: int = 720,
    report_path: Optional[str] = None,
) -> dict:
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return report_backend.page_add(
        Path(path), display_name=display_name, name=name, width=width, height=height
    )


def _page_delete(page_name: str, report_path: Optional[str] = None) -> dict:
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return report_backend.page_delete(Path(path), page_name)


def _page_set_background(
    page_name: str,
    color: str,
    transparency: int = 0,
    report_path: Optional[str] = None,
) -> dict:
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return report_backend.page_set_background(Path(path), page_name, color, transparency=transparency)


def _page_set_visibility(
    page_name: str,
    hidden: bool = False,
    report_path: Optional[str] = None,
) -> dict:
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return report_backend.page_set_visibility(Path(path), page_name, hidden=hidden)


def register_tools(mcp: FastMCP) -> None:
    for fn in (
        _page_list,
        _page_get,
        _page_add,
        _page_delete,
        _page_set_background,
        _page_set_visibility,
    ):
        mcp.tool(name="pbi_" + fn.__name__.lstrip("_"))(fn)
