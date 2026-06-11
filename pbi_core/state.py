from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class McpState:
    session: Optional[Any] = None
    report_path: Optional[str] = None


_state = McpState()


def get_state() -> McpState:
    return _state


def reset_state() -> None:
    _state.session = None
    _state.report_path = None
