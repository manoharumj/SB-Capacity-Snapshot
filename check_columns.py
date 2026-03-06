"""
Run this to see what columns are in your Excel files:
    .venv\Scripts\python.exe check_columns.py
"""
import pandas as pd

print("=== universe sheet columns ===")
df_u = pd.read_excel("data/fallback.xlsx", sheet_name="universe")
for c in df_u.columns:
    print(f"  {c}")

print("\n=== historical sheet columns ===")
df_h = pd.read_excel("data/fallback.xlsx", sheet_name="historical")
for c in df_h.columns:
    print(f"  {c}")
