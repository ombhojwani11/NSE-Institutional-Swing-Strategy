import os
import zipfile
import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
from calendar import monthrange

class MarketDataPipeline:
    """
    A robust data ingestion pipeline for extracting, cleaning, and formatting 
    daily exchange tick/EOD data from nested CSVs and ZIP archives.
    """
    
    def __init__(self, delivery_dir, futures_dir):
        self.delivery_dir = delivery_dir
        self.futures_dir = futures_dir

    @staticmethod
    def extract_from_zip(zip_path, filename):
        """
        Safely extracts specific instrument files (e.g., F&O tick data) 
        from daily compressed exchange archives.
        """
        try:
            with zipfile.ZipFile(zip_path) as z:
                with z.open(filename) as f:
                    df = pd.read_csv(f)
                    df.columns = df.columns.str.upper().str.strip()
                    return df
        except Exception as e:
            logging.warning(f"Failed to extract {filename} from {zip_path}: {e}")
            return None

    @staticmethod
    def try_read_csv(path):
        """Attempts to read and standardize CSV data, handling encoding/formatting anomalies."""
        try:
            df = pd.read_csv(path)
            df.columns = df.columns.str.upper().str.strip()
            return df
        except Exception as e:
            logging.warning(f"Failed to read CSV at {path}: {e}")
            return None

    @staticmethod
    def calculate_vwap(df, price_col, volume_col):
        """
        Calculates Volume Weighted Average Price (VWAP).
        Includes safe-handling for NaN values and division-by-zero errors.
        """
        try:
            if price_col in df.columns and volume_col in df.columns:
                price = pd.to_numeric(df[price_col], errors='coerce')
                volume = pd.to_numeric(df[volume_col], errors='coerce')
                
                # Filter out invalid or zero-volume rows
                valid = ~price.isna() & ~volume.isna() & (volume > 0)
                if valid.any():
                    return (price[valid] * volume[valid]).sum() / volume[valid].sum()
        except Exception:
            pass
        return float('nan')

    @staticmethod
    def calculate_percentage_change(df, cols, group_cols=None):
        """
        Calculates rolling percentage changes across dynamic groups 
        (e.g., specific expiries or strike prices).
        Handles market gaps, infinities, and NaN injections gracefully.
        """
        try:
            df_copy = df.copy()
            if group_cols:
                df_copy = df_copy.sort_values(group_cols + ["DATE"])
                for col in cols:
                    df_copy[f"{col}_CHANGE_%"] = df_copy.groupby(group_cols)[col].pct_change() * 100
            else:
                df_copy = df_copy.sort_values("DATE")
                for col in cols:
                    df_copy[f"{col}_CHANGE_%"] = df_copy[col].pct_change() * 100
            
            # Sanitize extreme volatility spikes (infinities)
            for col in cols:
                df_copy[f"{col}_CHANGE_%"] = (df_copy[f"{col}_CHANGE_%"]
                                          .replace([float('inf')], 1000)
                                          .replace([-float('inf')], -1000)
                                          .fillna(0)
                                          .clip(-1000, 1000)
                                          .round(2))
            return df_copy
        except Exception as e:
            logging.error(f"Error calculating percentage change: {e}")
            return df

    @staticmethod
    def get_trading_days(year, month):
        """
        Generates a standardized list of valid trading days (weekdays),
        filtering out weekends to align disparate datasets.
        """
        start_date = datetime(year, month, 1).date()
        _, last_day = monthrange(year, month)
        end_date = datetime(year, month, last_day).date()
        
        dates = []
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() < 5:  # Monday to Friday
                dates.append(current_date)
            current_date += timedelta(days=1)
        return sorted(dates)
