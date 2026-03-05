import pandas as pd
import numpy as np
from utils.transform import transform_data

def test_transform_data_cleaning():
    data = {
        "Title": ["Test", "Unknown Product"],
        "Price": ["$10", "$20"],
        "Rating": ["4.5 / 5", "Invalid Rating"],
        "Colors": ["3 Colors", "5 Colors"],
        "Size": ["Size: M", "Size: L"],
        "Gender": ["Gender: Men", "Gender: Women"],
        "timestamp": ["2024-01-01", "2024-01-01"]
    }

    df = pd.DataFrame(data)
    result = transform_data(df)

    assert len(result) == 1
    assert result.iloc[0]["Price"] == 10 * 16000
    assert isinstance(result.iloc[0]["Rating"], float)
    assert isinstance(result.iloc[0]["Colors"], (int, np.integer))
    assert result.iloc[0]["Size"] == "M"
    assert result.iloc[0]["Gender"] == "Men"

def test_transform_error():
    result = transform_data(None)
    assert isinstance(result, pd.DataFrame)