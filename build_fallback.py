"""
Run this once from your project root to create data/fallback.xlsx:

    .venv\Scripts\python.exe build_fallback.py

It reads your two existing Excel files and merges them into
data/fallback.xlsx with the sheet names the app expects.
"""

import pandas as pd
from pathlib import Path

UNIVERSE_FILE   = r"C:\Users\ManoharU\OneDrive - ShipBob Inc\Documents\Universe of capacity.xlsx"
HISTORICAL_FILE = r"C:\Users\ManoharU\OneDrive - ShipBob Inc\Documents\Historical sites capacity.xlsx"
OUTPUT_FILE     = Path("data/fallback.xlsx")

OUTPUT_FILE.parent.mkdir(exist_ok=True)

print("Reading Universe of capacity...")
df_universe = pd.read_excel(UNIVERSE_FILE)
print(f"  → {len(df_universe)} rows, columns: {list(df_universe.columns)}")

print("Reading Historical sites capacity...")
df_historical = pd.read_excel(HISTORICAL_FILE)
print(f"  → {len(df_historical)} rows, columns: {list(df_historical.columns)}")

print(f"Writing {OUTPUT_FILE}...")
with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
    df_universe.to_excel(writer,   sheet_name="universe",   index=False)
    df_historical.to_excel(writer, sheet_name="historical", index=False)

print("Done! data/fallback.xlsx is ready.")
