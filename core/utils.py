import pandas as pd
from pathlib import Path
from typing import Optional, Any
from rest_framework.exceptions import ValidationError
from pandas import DataFrame

def load_book(file: Path) -> pd.DataFrame:
    ext = Path(file.name).suffix.lower()
    if ext == '.xlsx':
        return pd.read_excel(file)
    elif ext == '.csv':
        return pd.read_csv(file)
    else:
        raise ValueError('サポートされていないファイル形式です。(.csv または .xlsx)')

def parse_int_or_none(raw: Any) -> Optional[int]:
    if raw is None:
        return None
    
    s = str(raw).strip().lower()
    
    if not s or s in ('nan', 'none'):
        return None
    
    try:
        return int(float(s))
    except (ValueError, TypeError):
        return None

def normalize_df(dataframe: DataFrame) -> DataFrame:
    return dataframe.rename(columns=lambda c: c.strip().lstrip('\ufeff') if isinstance(c, str) else c)

def require_columns(dataframe: DataFrame, required: set):
    missing = required - set(dataframe.columns)
    if missing:
        raise ValidationError({'header': f'欠落列: {", ".join(missing)}'})
