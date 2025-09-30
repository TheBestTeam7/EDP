
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from .io_monthly import read_monthly_txt
from .smoothing import running_mean_13

# --- Paths ---
BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"
OUT  = BASE / "outputs"
OUT.mkdir(exist_ok=True, parents=True)

RADIO_FILE = DATA / "Radio_flux_monthly_mean.txt"
SUNSPOT_FILE = DATA / "Sunspot_number_monthly_mean.txt"

def main():
    # Load
    df_F = read_monthly_txt(RADIO_FILE, "F10_7")
    df_R = read_monthly_txt(SUNSPOT_FILE, "R")

    # Outer merge on date to preserve spans
    df_all = pd.merge(df_R, df_F, on="date", how="outer").sort_values("date").reset_index(drop=True)

    # Apply smoothing separately
    df_all["R_smooth"] = running_mean_13(df_all["R"].to_numpy(dtype=float))
    df_all["F_smooth"] = running_mean_13(df_all["F10_7"].to_numpy(dtype=float))

    # Save merged CSV
    csv_path = OUT / "merged_timeseries_day1.csv"
    df_all.to_csv(csv_path, index=False)

    # Plot raw monthly
    plt.figure(figsize=(10, 5))
    plt.plot(df_all["date"], df_all["R"], label="Sunspot Number (monthly mean)")
    plt.plot(df_all["date"], df_all["F10_7"], label="F10.7 Radio Flux (monthly mean)")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.title("Monthly means: Sunspot Number vs F10.7")
    plt.legend()
    plt.tight_layout()
    fig1_path = OUT / "fig_raw_monthly.png"
    plt.savefig(fig1_path, dpi=200)
    plt.close()

    # Plot smoothed
    plt.figure(figsize=(10, 5))
    plt.plot(df_all["date"], df_all["R_smooth"], label="Sunspot Number (13-mo smoothed)")
    plt.plot(df_all["date"], df_all["F_smooth"], label="F10.7 Radio Flux (13-mo smoothed)")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.title("13-month smoothed: Sunspot Number vs F10.7")
    plt.legend()
    plt.tight_layout()
    fig2_path = OUT / "fig_smoothed.png"
    plt.savefig(fig2_path, dpi=200)
    plt.close()

    # Quick summary to Excel (optional)
    summary = pd.DataFrame({
        "Series": ["R", "F10.7"],
        "Start (raw)": [df_all["date"][df_all["R"].first_valid_index()] if df_all["R"].first_valid_index() is not None else None,
                        df_all["date"][df_all["F10_7"].first_valid_index()] if df_all["F10_7"].first_valid_index() is not None else None],
        "End (raw)": [df_all["date"][df_all["R"].last_valid_index()] if df_all["R"].last_valid_index() is not None else None,
                      df_all["date"][df_all["F10_7"].last_valid_index()] if df_all["F10_7"].last_valid_index() is not None else None],
        "Count (raw)": [df_all["R"].count(), df_all["F10_7"].count()],
        "Count (smoothed non-NA)": [np.isfinite(df_all["R_smooth"]).sum(), np.isfinite(df_all["F_smooth"]).sum()],
    })
    xlsx_path = OUT / "Day1_Summary.xlsx"
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as w:
        summary.to_excel(w, index=False, sheet_name="Summary")

    print("Saved:", csv_path)
    print("Saved:", fig1_path)
    print("Saved:", fig2_path)
    print("Saved:", xlsx_path)

if __name__ == "__main__":
    main()
