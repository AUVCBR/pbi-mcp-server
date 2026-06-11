# PBI Connection MCP — Reference

Use the `pbi-connection` MCP tools for ALL Power BI file operations.
Never edit .pbip JSON files manually.

## Layer guide

| Layer | Tools | Requires |
|-------|-------|----------|
| Report | visuals, pages, filters, bookmarks, formatting | `report_path` param only |
| Model | measures, DAX, tables, relationships, security | `pbi_connect` first |

## Connection

```
pbi_connect()                          # auto-discover Desktop port
pbi_connect(report_path="C:/x.pbip")  # also set default report path
pbi_connection_status()                # check if connected
```

## Common tasks

| Task | Tool |
|------|------|
| List pages | `pbi_page_list` |
| Add a visual | `pbi_visual_add(page_name, visual_type, x, y, width, height)` |
| Bind data to visual | `pbi_visual_bind(page_name, visual_name, role, table, column)` |
| Add page filter | `pbi_filters_add_categorical(page_name, field, values)` |
| Create a DAX measure | `pbi_measure_create(table, name, expression)` |
| Run DAX query | `pbi_dax_execute(query)` |
| Export model to TMDL | `pbi_database_export_tmdl(path)` |
| List supported visual types | `pbi_visual_types()` |

## New visual types

Add `templates/visuals/<TypeName>.json` — no code change needed.
`pbi_visual_types()` auto-discovers all templates in that folder.

## Batching writes

Set `sync_desktop=False` for multiple visual writes, then call `pbi_report_reload()` once at the end.

## Error patterns

| Error message | Fix |
|---------------|-----|
| "No active session" | Call `pbi_connect` first |
| "report_path required" | Pass `report_path` param or call `pbi_connect(report_path=...)` |
| "Power BI Desktop not found" | Open the .pbip file in Power BI Desktop first |

## MCP server location

`D:\My Own Project\Power Bi Connection\pbi-mcp-server\server.py`

## Registration (Claude Code settings)

```json
{
  "pbi-connection": {
    "type": "stdio",
    "command": "python",
    "args": ["D:/My Own Project/Power Bi Connection/pbi-mcp-server/server.py"]
  }
}
```

## Phase 2 (future)

A `power-bi-report-generator` skill (not yet built) will take `{dataset, instructions}`
and use these MCP tools to auto-generate a full `.pbip` report.
