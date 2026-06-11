# pbi-mcp-server

A custom [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that connects Claude Code to local Power BI `.pbip` files — giving Claude full read/write access to both the **report layer** (pages, visuals, filters) and the **semantic model layer** (measures, DAX, tables, relationships).

No Power BI REST API. No cloud. Works entirely against your local Power BI Desktop instance.

---

## Features

- **Zero-config connection** — `pbi_connect()` auto-discovers the open Power BI Desktop port and the active `.pbip` file path
- **Report layer** — add/delete/update visuals, bind data fields, manage pages, filters, bookmarks, and conditional formatting — all via direct PBIR JSON edits, no Desktop required
- **Model layer** — create/update measures, query DAX, list tables/columns/relationships, export TMDL — via live TOM/ADOMD.NET connection to the running Desktop instance
- **90 MCP tools** across 13 domains, all named `pbi_*`
- **Extensible visual types** — add a new `templates/visuals/<TypeName>.json` and `pbi_visual_types()` picks it up automatically, no code change needed
- **FastMCP 3.4.2** — modern Python MCP framework with full stdio transport

---

## Requirements

- Windows 10/11
- Power BI Desktop (MSI or Microsoft Store)
- Python 3.10+
- [Claude Code](https://claude.ai/code) (CLI, VS Code extension, or desktop app)

---

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/AUVCBR/pbi-mcp-server.git
cd pbi-mcp-server
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Unblock the bundled DLLs

Windows marks DLLs copied from other locations as unsafe. Unblock them once:

```powershell
Get-ChildItem ".\dlls\*" | Unblock-File
```

### 3. Register with Claude Code

Add to your project's `.mcp.json` (create it in your project root if it doesn't exist):

```json
{
  "mcpServers": {
    "pbi-connection": {
      "type": "stdio",
      "command": "C:/path/to/pbi-mcp-server/.venv/Scripts/python.exe",
      "args": ["C:/path/to/pbi-mcp-server/server.py"]
    }
  }
}
```

Or register globally via the Claude Code CLI:

```bash
claude mcp add pbi-connection --transport stdio \
  "C:/path/to/pbi-mcp-server/.venv/Scripts/python.exe" \
  "C:/path/to/pbi-mcp-server/server.py"
```

### 4. Connect

Open your `.pbip` file in Power BI Desktop, then in Claude Code:

```
Call pbi_connect()
```

Claude will auto-detect the Desktop port and the open file — no arguments needed.

---

## Tool Reference

### Connection (5 tools)

| Tool | Description |
|------|-------------|
| `pbi_connect` | Connect to Power BI Desktop. Auto-detects port and `.pbip` path. |
| `pbi_disconnect` | Close the active session. |
| `pbi_connection_status` | Check connection state and active report path. |
| `pbi_connections_list` | List saved connections. |
| `pbi_connections_last` | Show the most recently used connection. |

### Pages (6 tools)

`pbi_page_list` · `pbi_page_get` · `pbi_page_add` · `pbi_page_delete` · `pbi_page_set_background` · `pbi_page_set_visibility`

### Visuals (12 tools)

`pbi_visual_types` · `pbi_visual_list` · `pbi_visual_get` · `pbi_visual_add` · `pbi_visual_update` · `pbi_visual_delete` · `pbi_visual_bind` · `pbi_visual_bind_many` · `pbi_visual_bulk_update` · `pbi_visual_bulk_delete` · `pbi_visual_bulk_bind` · `pbi_visual_where`

### Filters (6 tools)

`pbi_filters_list` · `pbi_filters_add_categorical` · `pbi_filters_add_topn` · `pbi_filters_add_relative_date` · `pbi_filters_remove` · `pbi_filters_clear`

### Bookmarks (5 tools)

`pbi_bookmarks_list` · `pbi_bookmarks_get` · `pbi_bookmarks_add` · `pbi_bookmarks_delete` · `pbi_bookmarks_set_visibility`

### Formatting (5 tools)

`pbi_format_get` · `pbi_format_clear` · `pbi_format_background_gradient` · `pbi_format_background_conditional` · `pbi_format_background_measure`

### Model — requires `pbi_connect` (16 tools)

`pbi_measure_list` · `pbi_measure_get` · `pbi_measure_create` · `pbi_measure_update` · `pbi_measure_delete` · `pbi_table_list` · `pbi_table_get` · `pbi_column_list` · `pbi_relationship_list` · `pbi_relationship_create` · `pbi_hierarchy_list` · `pbi_hierarchy_create` · `pbi_hierarchy_delete` · `pbi_calc_group_list` · `pbi_calc_group_create` · `pbi_calc_group_delete`

### DAX (3 tools)

`pbi_dax_execute` · `pbi_dax_validate` · `pbi_dax_clear_cache`

### Database & Transactions (8 tools)

`pbi_database_list` · `pbi_database_export_tmdl` · `pbi_database_import_tmdl` · `pbi_database_export_tmsl` · `pbi_database_diff_tmdl` · `pbi_transaction_begin` · `pbi_transaction_commit` · `pbi_transaction_rollback`

### Security (8 tools)

`pbi_security_role_list` · `pbi_security_role_get` · `pbi_security_role_create` · `pbi_security_role_delete` · `pbi_security_role_add_filter` · `pbi_perspective_list` · `pbi_perspective_create` · `pbi_perspective_delete`

### Data (7 tools)

`pbi_partition_list` · `pbi_partition_get` · `pbi_partition_update` · `pbi_expression_get` · `pbi_expression_list` · `pbi_calendar_list` · `pbi_calendar_define` · `pbi_culture_set`

### Diagnostics (5 tools)

`pbi_trace_start` · `pbi_trace_stop` · `pbi_trace_fetch` · `pbi_trace_export` · `pbi_model_stats`

---

## Architecture

```
pbi-mcp-server/
├── server.py              # FastMCP entry point — registers all 90 tools
├── pbi_core/              # Backend engines (TOM, ADOMD, PBIR JSON)
│   ├── dotnet_loader.py   # .NET CLR bootstrap for pythonnet
│   ├── session.py         # Connection management
│   ├── tom_backend.py     # Tabular Object Model operations
│   ├── adomd_backend.py   # DAX query execution
│   ├── report_backend.py  # PBIR JSON read/write
│   ├── visual_backend.py  # Visual add/update/bind
│   └── ...
├── tools/                 # 13 MCP tool modules (one per domain)
├── dlls/                  # Bundled Microsoft Analysis Services DLLs
├── templates/visuals/     # 32 JSON visual type templates
└── tests/                 # Unit tests (26 passing)
```

**Two-layer design:**
- **Report layer** (`tools/page_tools.py`, `visual_tools.py`, etc.) — reads/writes PBIR JSON directly, Power BI Desktop does not need to be open
- **Model layer** (`tools/model_tools.py`, `dax_tools.py`, etc.) — connects to Power BI Desktop's embedded Analysis Services instance via pythonnet + Microsoft DLLs

---

## Adding New Visual Types

Drop a new JSON template into `templates/visuals/`:

```bash
cp my_custom_visual.json templates/visuals/myCustomVisual.json
```

`pbi_visual_types()` will immediately include it. No code changes needed.

---

## Development

```bash
# Run tests
.venv\Scripts\pytest tests\ -v

# Verify server starts
.venv\Scripts\python server.py
```

---

## Tech Stack

| Component | Library |
|-----------|---------|
| MCP framework | [FastMCP](https://github.com/jlowin/fastmcp) 3.4.2 |
| .NET interop | [pythonnet](https://pythonnet.github.io/) 3.1.0rc0 |
| Analysis Services | Microsoft.AnalysisServices.Tabular (bundled DLLs) |
| ADOMD.NET | Microsoft.AnalysisServices.AdomdClient (bundled) |
| Report format | PBIR JSON (Power BI Enhanced Report Format) |

---

## License

MIT
