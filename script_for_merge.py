"""Rebuild the India oil-price/inflation dataset from the original source files.

Expected input files in ./data/raw/:
  Crude-Oil-Price-(Indian Basket)-Historical.xlsx
  r45_consumer_price_index.csv
  Exchange Rate of the Indian Rupee vis-à-vis the SDR, US Dollar, Pound Sterling, Euro and Japanese Yen (Monthly Average and end-Month Rates).xlsx

Run from the project directory:
  python build_oil_inflation_dataset.py

Requires pandas and openpyxl: pip install pandas openpyxl
"""
from pathlib import Path
import re
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
PROCESSED.mkdir(parents=True, exist_ok=True)

OIL_FILE = RAW / "Crude-Oil-Price-(Indian Basket)-Historical.xlsx"
CPI_FILE = RAW / "r45_consumer_price_index.csv"
FX_FILE = RAW / "Exchange Rate of the Indian Rupee vis-à-vis the SDR, US Dollar, Pound Sterling, Euro and Japanese Yen (Monthly Average and end-Month Rates).xlsx"

START = pd.Timestamp("2013-01-01")
END = pd.Timestamp("2025-12-01")

# ---------------------------------------------------------------------------
# 1) PPAC oil prices: rows are financial years (e.g. 2013-14), and the 12
#    monthly values run April, May, ..., December, January, February, March.
#    Do NOT use the odd date-like column headings as the observation dates.
# ---------------------------------------------------------------------------
oil_raw = pd.read_excel(OIL_FILE, header=None)
oil_rows = oil_raw.iloc[13:].copy()  # first data row follows the title/header block
oil_rows = oil_rows[oil_rows.iloc[:, 0].astype(str).str.match(r"^\d{4}-\d{2}$", na=False)]

oil_records = []
for _, row in oil_rows.iterrows():
    financial_year = str(row.iloc[0]).strip()
    start_year = int(financial_year.split("-")[0])
    for month_position in range(12):
        value = pd.to_numeric(row.iloc[1 + month_position], errors="coerce")
        if pd.isna(value):
            continue
        # Positions 0..8 = Apr..Dec of start_year; 9..11 = Jan..Mar next year.
        month_number = month_position + 4
        year_number = start_year
        if month_number > 12:
            month_number -= 12
            year_number += 1
        oil_records.append({
            "date": pd.Timestamp(year=year_number, month=month_number, day=1),
            "oil_price_usd_bbl": float(value),
        })

oil = pd.DataFrame(oil_records).sort_values("date").reset_index(drop=True)
if oil.empty or oil["date"].duplicated().any():
    raise ValueError("Oil extraction failed or produced duplicate months; inspect PPAC workbook layout.")

# ---------------------------------------------------------------------------
# 2) RBI CPI: retain only 'A) General Index'. In this CSV, c1 is the month,
#    c2 is the commodity description, c8 is Combined Index, and c9 is
#    Combined Inflation (%). Source rows are in reverse chronological order.
# ---------------------------------------------------------------------------
cpi_raw = pd.read_csv(CPI_FILE, dtype=str)
cpi_rows = cpi_raw[cpi_raw["c2"].astype(str).str.strip().eq("A) General Index")].copy()
cpi_rows["date"] = pd.to_datetime(
    cpi_rows["c1"].astype(str).str.title(), format="%b-%Y", errors="coerce"
)
cpi_rows["cpi_combined_index"] = pd.to_numeric(cpi_rows["c8"], errors="coerce")
cpi_rows["cpi_inflation_yoy_pct"] = pd.to_numeric(cpi_rows["c9"], errors="coerce")
cpi = cpi_rows[["date", "cpi_combined_index", "cpi_inflation_yoy_pct"]].dropna(subset=["date"])
cpi = cpi.sort_values("date").reset_index(drop=True)
if cpi["date"].duplicated().any():
    raise ValueError("CPI extraction produced duplicate months; inspect CPI file.")

# ---------------------------------------------------------------------------
# 3) RBI exchange rates: extract the 'US Dollar' Average column, not its
#    End-month column. The workbook's displayed month label is in column 3
#    (zero-based index 2); US Dollar Average is column 6 (index 5).
# ---------------------------------------------------------------------------
fx_raw = pd.read_excel(FX_FILE, header=None)
fx_rows = fx_raw.iloc[8:].copy()  # skip report title and multi-row headings
period_labels = fx_rows.iloc[:, 2].astype(str).str.strip()
fx_rows = fx_rows[period_labels.str.match(r"^[A-Za-z]{3}-\d{4}$", na=False)].copy()
fx_rows["date"] = pd.to_datetime(
    fx_rows.iloc[:, 2].astype(str).str.strip(), format="%b-%Y", errors="coerce"
)
fx_rows["usd_inr_monthly_avg"] = pd.to_numeric(fx_rows.iloc[:, 5], errors="coerce")
fx = fx_rows[["date", "usd_inr_monthly_avg"]].dropna(subset=["date", "usd_inr_monthly_avg"])
fx = fx.sort_values("date").reset_index(drop=True)
if fx["date"].duplicated().any():
    raise ValueError("Exchange-rate extraction produced duplicate months; inspect workbook.")

# ---------------------------------------------------------------------------
# 4) Merge by calendar month, not by row position. Use the common intersection
#    of months and then retain the stated target sample.
# ---------------------------------------------------------------------------
merged = oil.merge(cpi, on="date", how="inner", validate="one_to_one")
merged = merged.merge(fx, on="date", how="inner", validate="one_to_one")
merged = merged.loc[merged["date"].between(START, END)].sort_values("date").reset_index(drop=True)

# ---------------------------------------------------------------------------
# 5) Construct transformations AFTER restricting to Jan 2013-Dec 2025, so
#    the first in-sample monthly changes are missing by definition.
# ---------------------------------------------------------------------------
merged["oil_change_pct"] = merged["oil_price_usd_bbl"].pct_change() * 100
merged["oil_log_return_pct"] = np.log(merged["oil_price_usd_bbl"]).diff() * 100
# Simple descriptive volatility proxy: rolling SD of the current and previous
# two monthly oil log changes. This is not a GARCH conditional-volatility model.
merged["oil_volatility_3m"] = merged["oil_log_return_pct"].rolling(window=3, min_periods=3).std()
merged["usd_inr_change_pct"] = merged["usd_inr_monthly_avg"].pct_change() * 100

columns = [
    "date", "oil_price_usd_bbl", "cpi_combined_index", "cpi_inflation_yoy_pct",
    "usd_inr_monthly_avg", "oil_change_pct", "oil_log_return_pct",
    "oil_volatility_3m", "usd_inr_change_pct",
]
merged = merged[columns]

# Master file keeps 2013, even though the supplied CPI source has no YoY
# inflation values for 2013. Analysis file starts in Jan 2014, giving 144 rows.
master_path = PROCESSED / "oil_inflation_india_master_2013_2025.csv"
analysis_path = PROCESSED / "oil_inflation_india_analysis_ready_2014_2025.csv"
merged.to_csv(master_path, index=False, date_format="%Y-%m-%d")
analysis = merged.loc[merged["date"] >= pd.Timestamp("2014-01-01")].copy()
analysis.to_csv(analysis_path, index=False, date_format="%Y-%m-%d")

# Compact audit report to make assumptions/results visible.
print("Source rows after extraction:")
print(f"  Oil monthly series: {len(oil)} rows, {oil['date'].min():%Y-%m} to {oil['date'].max():%Y-%m}")
print(f"  CPI General Index:  {len(cpi)} rows, {cpi['date'].min():%Y-%m} to {cpi['date'].max():%Y-%m}")
print(f"  USD average:        {len(fx)} rows, {fx['date'].min():%Y-%m} to {fx['date'].max():%Y-%m}")
print(f"  Master:             {len(merged)} rows, {merged['date'].min():%Y-%m} to {merged['date'].max():%Y-%m}")
print(f"  Analysis:            {len(analysis)} rows, {analysis['date'].min():%Y-%m} to {analysis['date'].max():%Y-%m}")
print("  Missing CPI YoY in master:", int(merged["cpi_inflation_yoy_pct"].isna().sum()))
print("  Duplicate master months:", int(merged["date"].duplicated().sum()))
print("Wrote:")
print(" ", master_path)
print(" ", analysis_path)
