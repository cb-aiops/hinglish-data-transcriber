import pandas as pd

def read_csv(file_path):
    """Reads a CSV file into a DataFrame."""
    return pd.read_csv(file_path)

def write_csv(df, file_path):
    """Writes a DataFrame to a CSV file with BOM for Excel compatibility."""
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
