
import pandas as pd
from pathlib import Path

def read_monthly_txt(path: Path, value_col: str) -> pd.DataFrame:
    """
    Read whitespace-separated monthly data with columns: year, month, value.
    Returns DataFrame with columns: ['date', value_col] where date = first day of month.
    Lines starting with '#' are ignored.
    """
    df = pd.read_csv(path, sep=r"\s+", header=None, comment="#", engine="python")
    if df.shape[1] < 3:
        raise ValueError(f"File {path.name} should have at least 3 columns (year, month, value). Got shape {df.shape}.")
    df = df.iloc[:, :3]
    df.columns = ["year", "month", value_col]
    df["date"] = pd.to_datetime(dict(year=df["year"].astype(int),
                                     month=df["month"].astype(int),
                                     day=1))
    df = df[["date", value_col]].sort_values("date").reset_index(drop=True)
    return df
