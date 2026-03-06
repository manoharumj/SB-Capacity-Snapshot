"""
Dumps the raw historical query output to Excel for validation.
Run from project root:
    .venv\Scripts\python.exe dump_historical.py
"""
import pandas as pd
from backend.config import settings
from backend.db import run_query, load_sql

print("Running historical query (MFA prompt may appear)...")
df = run_query(load_sql("historical.sql"))

print(f"Rows: {len(df):,}  |  Columns: {list(df.columns)}")
print(f"Weekstart range: {df['weekstart'].min()} → {df['weekstart'].max()}")
print(f"Sites: {df['SiteName'].nunique()}")

out = "data/historical_raw.xlsx"
df.to_excel(out, index=False)
print(f"\nSaved to {out}")
