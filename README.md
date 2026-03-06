# Capacity Intelligence Dashboard

Internal fulfillment network capacity dashboard.
**Stack:** FastAPI (Python) + vanilla JS + Chart.js · Data: Azure SQL

---

## Folder Structure

```
capacity-dashboard/
├── backend/
│   ├── main.py          # FastAPI app — all API routes
│   ├── db.py            # Azure SQL connection + query runner
│   ├── transform.py     # All aggregation & metric logic (pandas)
│   ├── cache.py         # In-memory TTL cache
│   ├── config.py        # Settings from .env
│   └── queries/
│       ├── universe.sql     # Universe of Capacity query
│       └── historical.sql   # Historical Capacity query
├── frontend/
│   ├── index.html       # Dashboard UI
│   ├── js/
│   │   ├── api.js       # fetch() calls to backend
│   │   ├── filters.js   # Filter state + applyFilters()
│   │   ├── charts.js    # All Chart.js logic
│   │   └── table.js     # Table rendering
│   └── css/
│       └── styles.css
├── .env                 # DB credentials — DO NOT commit
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Prerequisites

- Python 3.11+
- [ODBC Driver 18 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
- VS Code (recommended extensions: Python, REST Client)

### 2. Create virtual environment

```bash
cd capacity-dashboard
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure credentials

Edit `.env` with your Azure SQL details:

```env
DB_SERVER=your-server.database.windows.net
DB_DATABASE=your-database
DB_USERNAME=your-user
DB_PASSWORD=your-password
```

### 5. Add your SQL queries

Paste your existing queries into:
- `backend/queries/universe.sql`
- `backend/queries/historical.sql`

Make sure the output column names match the aliases in each file's comments.
The `historical.sql` file should alias `Occupied_cube_capacity AS Product_cube_stored`.

### 6. Run the server

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Open **http://127.0.0.1:8000** in your browser.

---

## API Endpoints

| Endpoint        | Description                                      |
|-----------------|--------------------------------------------------|
| `GET /`         | Serves the dashboard HTML                        |
| `GET /api/all`  | All dashboard data in one call (used on load)    |
| `GET /api/sites`| Latest snapshot per site                         |
| `GET /api/trend`| Weekly trend by region                           |
| `GET /api/regions`| Region summary                                 |
| `GET /api/refresh`| Force cache bust + re-run SQL queries          |
| `GET /api/health` | Liveness check + cache status                  |

Interactive docs: **http://127.0.0.1:8000/docs**

---

## Metric Definitions

| Metric | Formula | Notes |
|--------|---------|-------|
| Loc Cube Util % | `Total_cube_capacity_occupied ÷ Total_cube_capacity` | Bounded ≤ 100% |
| Product Cube % | `Product_cube_stored ÷ Total_cube_capacity` | Can exceed 100% |
| Loc Fill Rate % | `Occupied_reachable_locs ÷ Total_reachable_locs` | Bounded ≤ 100% |
| Outside Map | `CubeStoredOutsideMap > 0` | Product beyond WMS mapped locations |
| Sellable Cube | `Product_cube_stored − Packaging_mat_cube` | Net sellable volume |
| SKUs (zonal) | `SUM(dist_SKUs)` across TypeIds | Note: cross-zone duplicates possible |

---

## Cache

Data is cached in memory for **60 minutes** by default (set `CACHE_TTL_MINUTES` in `.env`).

Force a refresh via the **↻ Refresh** button in the dashboard, or:
```
GET http://127.0.0.1:8000/api/refresh
```

---

## Adding New Metrics

1. Add the field in `backend/transform.py` inside `aggregate_site_week()`
2. It will automatically appear in `to_records()` and flow through to the API
3. Reference it by name in `frontend/js/charts.js` or `table.js`
