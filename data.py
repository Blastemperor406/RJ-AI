# data.py
import pandas as pd

def load_songs_data(file_path):
    """Load song data from a CSV file."""
    return pd.read_csv(file_path)
