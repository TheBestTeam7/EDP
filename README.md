# EDP
Sun
## Structure
```
main/
  data/
    Radio_flux_monthly_mean.txt
    Sunspot_number_monthly_mean.txt
  outputs/
    ... (generated figures + CSV)
  src/
    io_monthly.py
    smoothing.py
    day1_pipeline.py
  report/
    (reserved for figures if you want)
  README.md
  requirements.txt
```

## How to run
1) Copy your two `.txt` files into `data/` (or use the ones here).
2) (Optional) Create venv, then install deps:
   ```bash
   pip install -r requirements.txt
   ```
3) Run:
   ```bash
   python -m src.day1_pipeline
   ```
4) See results in `outputs/`:
   - `fig_raw_monthly.png`
   - `fig_smoothed.png`
   - `merged_timeseries_day1.csv`
   - `Day1_Summary.xlsx` (optional tabular summary)

## Notes
- The 13‑month running mean follows the assignment’s weights:
  - Full window of 13 months: edge weights = 1/24, inner 11 months = 1/12 each
  - Incomplete windows near boundaries: simple arithmetic mean of available points
- The plotting is minimal and readable; feel free to tweak styles in the code.
