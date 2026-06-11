from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fastmcp import FastMCP

mcp = FastMCP(
    "pbi-connection",
    instructions=(
        "MCP server for Power BI .pbip files. "
        "Report-layer tools (visuals, pages, filters) work without a connection. "
        "Model-layer tools (measures, DAX, tables) require pbi_connect first."
    ),
)


def _register_all() -> None:
    from tools.connection_tools import register_tools as reg_conn
    from tools.report_tools import register_tools as reg_report
    from tools.page_tools import register_tools as reg_page
    from tools.visual_tools import register_tools as reg_visual
    from tools.filter_tools import register_tools as reg_filter
    from tools.bookmark_tools import register_tools as reg_bookmark
    from tools.format_tools import register_tools as reg_format
    from tools.model_tools import register_tools as reg_model
    from tools.dax_tools import register_tools as reg_dax
    from tools.database_tools import register_tools as reg_db
    from tools.security_tools import register_tools as reg_sec
    from tools.data_tools import register_tools as reg_data
    from tools.diagnostics_tools import register_tools as reg_diag

    for reg in (
        reg_conn, reg_report, reg_page, reg_visual, reg_filter,
        reg_bookmark, reg_format, reg_model, reg_dax, reg_db,
        reg_sec, reg_data, reg_diag,
    ):
        reg(mcp)


_register_all()


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
