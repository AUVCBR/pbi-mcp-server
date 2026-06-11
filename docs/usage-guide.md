# PBI MCP Server — Usage Guide

A practical reference for using `pbi-connection` MCP tools with Claude Code.  
All examples are prompts you type to Claude — Claude calls the tools for you.

---

## Table of Contents

1. [Connecting](#1-connecting)
2. [Pages](#2-pages)
3. [Visuals](#3-visuals)
4. [Binding Data to Visuals](#4-binding-data-to-visuals)
5. [Filters](#5-filters)
6. [Bookmarks](#6-bookmarks)
7. [Conditional Formatting](#7-conditional-formatting)
8. [Measures](#8-measures)
9. [DAX Queries](#9-dax-queries)
10. [Tables, Columns & Relationships](#10-tables-columns--relationships)
11. [TMDL Export / Import](#11-tmdl-export--import)
12. [Security Roles](#12-security-roles)
13. [Batch Operations](#13-batch-operations)
14. [Common Errors & Fixes](#14-common-errors--fixes)
15. [Layer Reference](#15-layer-reference)

---

## 1. Connecting

### Auto-connect (recommended)

Open your `.pbip` file in Power BI Desktop, then:

```
Connect to Power BI
```

Claude calls `pbi_connect()` with no arguments. It auto-detects:
- The Analysis Services port from the running Desktop process
- The open `.pbip` report path from the PBIDesktop command line

Response confirms both:
```json
{
  "status": "connected",
  "data_source": "localhost:54909",
  "catalog": "2950e0e1-...",
  "report_path": "D:\\Reports\\Sales.Report\\definition",
  "report_path_auto_detected": true
}
```

### Manual connect (multiple files open)

If you have multiple `.pbip` files open in different Desktop windows:

```
Connect to Power BI with report_path "D:\Reports\Sales\Sales.Report\definition"
```

> **Note:** `report_path` must point to the `.Report/definition` folder, **not** the `.pbip` file itself.

### Check connection status

```
What's the current Power BI connection status?
```

### Disconnect

```
Disconnect from Power BI
```

---

## 2. Pages

### List all pages

```
List all pages in my report
```

Returns page names, IDs, dimensions, visual count, and visibility.

### Add a page

```
Add a new page called "Executive Summary"
```

```
Add a 1920x1080 page called "Drill Through - Patient"
```

### Delete a page

```
Delete the "Page 1" page
```

### Hide / show a page

```
Hide the "Drill Through - Patient" page
```

```
Make the "Drill Through - Patient" page visible
```

### Set page background color

```
Set the background of the "Overview" page to #F5F5F5
```

---

## 3. Visuals

### See available visual types

```
What visual types are supported?
```

Returns all 32 built-in types: `barChart`, `lineChart`, `clusteredColumnChart`, `tableEx`, `card`, `slicer`, `kpi`, `gauge`, `donutChart`, `scatterChart`, `treemap`, `waterfallChart`, `ribbonChart`, `funnelChart`, `pivotTable`, `multiRowCard`, `areaChart`, `shape`, `textbox`, `image`, `pageNavigator`, `cardNew`, `cardVisual`, etc.

### Add a visual

```
Add a bar chart to the Overview page at position x=100, y=50, width=400, height=300
```

```
Add a KPI card to the "Executive Summary" page at x=0, y=0, 200x150
```

### List visuals on a page

```
List all visuals on the Overview page
```

### Get a specific visual

```
Get the details of visual abc123 on the Overview page
```

### Move or resize a visual

```
Move visual abc123 on Overview to x=200, y=100
```

```
Resize visual abc123 on Overview to 600x400
```

### Hide / show a visual

```
Hide visual abc123 on the Overview page
```

### Delete a visual

```
Delete visual abc123 from the Overview page
```

### Find visuals by type

```
Find all bar charts on the Overview page
```

---

## 4. Binding Data to Visuals

Binding connects a table field or measure to a visual's data role (axis, legend, values, etc.).

### Single bind

```
Bind the Category axis of visual abc123 on Overview to Dim_Department[Department_Name]
```

```
Bind the Values role of the bar chart to the TotalRevenue measure from the _Measure table
```

For measures, specify `is_measure=true`:

```
Bind the Y Axis of visual abc123 to _Measure[Total Revenue] — it's a measure
```

### Common role names by visual type

| Visual | Common roles |
|--------|-------------|
| Bar / Column chart | `Category`, `Y`, `Series` |
| Line chart | `Category`, `Y`, `Series` |
| Card / KPI | `Y` |
| Slicer | `Field` |
| Table / Matrix | `Values`, `Rows`, `Columns` |
| Scatter chart | `X`, `Y`, `Details`, `Size` |
| Donut / Pie | `Category`, `Y` |
| Gauge | `Y`, `MinValue`, `MaxValue`, `TargetValue` |
| Map | `Location`, `Size`, `Color` |

> Use `pbi_visual_get` to inspect a visual's current binding structure if unsure of role names.

---

## 5. Filters

### List filters on a page

```
List all filters on the Overview page
```

### List filters on a specific visual

```
List filters on visual abc123 on the Overview page
```

### Add a categorical filter

```
Add a filter on the Overview page for Dim_Department[Department_Name] = "Cardiology", "Emergency"
```

### Add a Top N filter

```
Add a Top 10 filter on the Overview page for Dim_Doctor[Doctor_Name] ordered by _Measure[Total Visits]
```

### Add a relative date filter

```
Add a relative date filter on the Overview page for Dim_Date[Date] — last 3 months
```

Time units: `days`, `weeks`, `months`, `years`

### Remove a specific filter

```
Remove the Department_Name filter from the Overview page
```

### Clear all filters on a page

```
Clear all filters on the Overview page
```

---

## 6. Bookmarks

### List all bookmarks

```
List all bookmarks in the report
```

### Add a bookmark

```
Add a bookmark called "Cardiology View" pointing to the Overview page
```

### Delete a bookmark

```
Delete the "Cardiology View" bookmark
```

### Set visual visibility inside a bookmark

```
In the "Cardiology View" bookmark, hide visual abc123 on the Overview page
```

---

## 7. Conditional Formatting

### Get current formatting

```
Get the formatting of visual abc123 on the Overview page
```

### Gradient background (e.g. heat map)

```
Apply a gradient background to visual abc123 on Overview — min color #white, max color #FF0000
```

### Rules-based conditional formatting

```
Apply conditional background to visual abc123 on Overview:
- If value < 50: red (#FF4444)
- If value 50–80: yellow (#FFD700)
- If value > 80: green (#44BB44)
```

### Measure-driven formatting

```
Apply measure-driven background to visual abc123 using the [BackgroundColor] measure
```

### Clear all formatting

```
Clear conditional formatting from visual abc123 on Overview
```

---

## 8. Measures

> Requires `pbi_connect()` — Power BI Desktop must be open.

### List all measures

```
List all measures in the model
```

### List measures in a specific table

```
List measures in the _Measure table
```

### Get a measure

```
Get the expression for the "Total Revenue" measure
```

### Create a measure

```
Create a measure called "Total Visits" in the _Measure table:
COUNTROWS(Fact_Patient_Visits)
```

With format string:

```
Create a measure "Avg Length of Stay" in _Measure:
AVERAGE(Fact_Patient_Visits[Length_of_Stay])
Format as: "0.0 days"
```

### Update a measure

```
Update the "Total Visits" measure expression to:
CALCULATE(COUNTROWS(Fact_Patient_Visits), Fact_Patient_Visits[Status] = "Completed")
```

### Delete a measure

```
Delete the "Total Visits" measure from the _Measure table
```

---

## 9. DAX Queries

> Requires `pbi_connect()`.

### Run a DAX query

```
Run this DAX query:
EVALUATE
SUMMARIZECOLUMNS(
    Dim_Department[Department_Name],
    "_Total Visits", [Total Visits]
)
ORDER BY [_Total Visits] DESC
```

### Validate a DAX expression (without running it)

```
Validate this DAX expression: CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(Dim_Date[Date]))
```

### Clear the model cache

```
Clear the Power BI model cache
```

---

## 10. Tables, Columns & Relationships

> Requires `pbi_connect()`.

### List all tables

```
List all tables in the model
```

### List columns in a table

```
List all columns in Fact_Patient_Visits
```

### List all relationships

```
List all relationships in the model
```

### Create a relationship

```
Create a relationship from Fact_Patient_Visits[Department_ID] to Dim_Department[Department_ID]
```

### List hierarchies

```
List hierarchies in the Dim_Date table
```

---

## 11. TMDL Export / Import

TMDL (Tabular Model Definition Language) is a text-based format for the full semantic model — useful for version control and diffing.

> Requires `pbi_connect()`.

### Export to TMDL

```
Export the model TMDL to D:\exports\MyModel_tmdl
```

Creates a folder with one `.tmdl` file per table, plus `model.tmdl` and `database.tmdl`.

### Import from TMDL

```
Import TMDL from D:\exports\MyModel_tmdl into the model
```

### Diff two TMDL exports

```
Show the diff between D:\exports\before_tmdl and D:\exports\after_tmdl
```

Useful before/after comparing model changes.

### Export as TMSL (JSON)

```
Export the model as TMSL JSON
```

---

## 12. Security Roles

> Requires `pbi_connect()`.

### List roles

```
List all security roles in the model
```

### Create a role

```
Create a security role called "Region Managers"
```

### Add a row-level security filter

```
Add an RLS filter to the "Region Managers" role on Dim_Region:
[Region_Manager_Email] = USERPRINCIPALNAME()
```

### Delete a role

```
Delete the "Region Managers" security role
```

---

## 13. Batch Operations

When making many visual changes at once, set `sync_desktop=False` on all but the last call to avoid Desktop reloading after every single write.

```
Add 3 visuals to the Overview page — a bar chart, a line chart, and a KPI card.
Don't sync after each one, just sync at the end.
```

Claude will use `sync_desktop=False` on the first two visuals and `sync_desktop=True` (or a final reload) on the last.

### Bulk update visual positions

```
Move all visuals on the Overview page 50px to the right
```

### Bulk delete visuals

```
Delete all visuals on "Page 1"
```

### Bulk bind fields

```
Bind these fields to visual abc123 on Overview:
- Category axis → Dim_Department[Department_Name]
- Y axis → _Measure[Total Visits]
- Series → Dim_Region[Region_Name]
```

---

## 14. Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `"No active session"` | Model-layer tool called before connecting | Call `pbi_connect()` first |
| `"report_path required"` | Report-layer tool with no path set | Pass `report_path` param or reconnect with `pbi_connect()` |
| `"Power BI Desktop not found"` | Desktop isn't running | Open your `.pbip` in Power BI Desktop |
| `"Could not load assembly"` | DLLs blocked by Windows | Run `Get-ChildItem ".\dlls\*" \| Unblock-File` once |
| `"The runtime has already been loaded"` | CLR crashed on a previous call | Reconnect `pbi-connection` in the MCP panel |
| `"Visual type not supported"` | Template doesn't exist | Check `pbi_visual_types()` for valid names |
| Empty page list `{"result":[]}` | Wrong `report_path` — pointing to `.pbip` not `.Report\definition` | Use path ending in `.Report\definition` |

---

## 15. Layer Reference

| Layer | Tools | Power BI Desktop required? |
|-------|-------|---------------------------|
| **Report** | pages, visuals, filters, bookmarks, formatting | No — edits PBIR JSON directly |
| **Model** | measures, DAX, tables, columns, relationships, TMDL, security, diagnostics | **Yes** — needs live TOM/ADOMD connection |

### Report path format

```
D:\Reports\MyReport\MyReport.Report\definition
                    ─────────────────────────────
                    NOT the .pbip file itself
```

### Typical session flow

```
1. Open .pbip in Power BI Desktop
2. pbi_connect()                          ← auto-detects everything
3. pbi_page_list()                        ← see what pages exist
4. pbi_visual_add(...)                    ← add visuals
5. pbi_visual_bind(...)                   ← bind data fields
6. pbi_measure_create(...)                ← add DAX measures
7. pbi_dax_execute(...)                   ← validate results
8. pbi_database_export_tmdl(...)          ← snapshot model
```
