from __future__ import annotations
from pathlib import Path
from typing import Optional
from fastmcp import FastMCP
from pbi_core import bookmark_backend
from pbi_core.state import get_state


def _resolve_path(p: Optional[str]) -> Optional[str]:
    return p or get_state().report_path


def _no_path_error() -> dict:
    return {"status": "error", "message": "report_path required"}


def _w(r):
    return {"items": r, "count": len(r)} if isinstance(r, list) else r


def _bookmarks_list(report_path: Optional[str] = None) -> list | dict:
    """List all bookmarks in the report. Note: bookmarks are report-level, not page-level."""
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return _w(bookmark_backend.bookmark_list(Path(path)))


def _bookmarks_get(bookmark_name: str, report_path: Optional[str] = None) -> dict:
    """Get full data for a single bookmark by name."""
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return bookmark_backend.bookmark_get(Path(path), bookmark_name)


def _bookmarks_add(
    display_name: str,
    target_page: str,
    name: Optional[str] = None,
    report_path: Optional[str] = None,
) -> dict:
    """Create a new bookmark pointing to the target page."""
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return bookmark_backend.bookmark_add(Path(path), display_name=display_name, target_page=target_page, name=name)


def _bookmarks_delete(bookmark_name: str, report_path: Optional[str] = None) -> dict:
    """Delete a bookmark by name."""
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return bookmark_backend.bookmark_delete(Path(path), bookmark_name)


def _bookmarks_set_visibility(
    bookmark_name: str,
    page_name: str,
    visual_name: str,
    hidden: bool = False,
    report_path: Optional[str] = None,
) -> dict:
    """Set a visual's hidden/visible state inside a bookmark's explorationState."""
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return bookmark_backend.bookmark_set_visibility(
        Path(path), bookmark_name, page_name=page_name, visual_name=visual_name, hidden=hidden
    )


def register_tools(mcp: FastMCP) -> None:
    for fn in (
        _bookmarks_list,
        _bookmarks_get,
        _bookmarks_add,
        _bookmarks_delete,
        _bookmarks_set_visibility,
    ):
        mcp.tool(name="pbi_" + fn.__name__.lstrip("_"))(fn)
