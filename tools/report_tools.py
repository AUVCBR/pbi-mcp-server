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


def _report_create(
    target_path: str,
    name: str,
    dataset_path: Optional[str] = None,
) -> dict:
    return report_backend.report_create(
        Path(target_path), name=name, dataset_path=dataset_path
    )


def _report_info(report_path: Optional[str] = None) -> dict:
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return report_backend.report_info(Path(path))


def _report_validate(report_path: Optional[str] = None) -> dict:
    path = _resolve_path(report_path)
    if not path:
        return _no_path_error()
    return report_backend.report_validate(Path(path))


def register_tools(mcp: FastMCP) -> None:
    for fn in (_report_create, _report_info, _report_validate):
        mcp.tool(name="pbi_" + fn.__name__.lstrip("_"))(fn)
