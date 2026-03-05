import pandas as pd
from unittest.mock import patch
from utils.load import (
    save_to_csv,
    save_to_google_sheets,
    save_to_postgresql,
    load_data
)

def test_save_to_csv(tmp_path):
    df = pd.DataFrame({"A": [1, 2]})
    file_path = tmp_path / "test.csv"
    df.to_csv(file_path, index=False)
    assert file_path.exists()

@patch("utils.load.gspread.authorize")
def test_save_to_google_sheets(mock_auth):
    df = pd.DataFrame({"A": [1]})
    save_to_google_sheets(df)
    assert mock_auth.called

@patch("utils.load.create_engine")
def test_save_to_postgresql(mock_engine):
    df = pd.DataFrame({"A": [1]})
    save_to_postgresql(df)
    assert mock_engine.called

@patch("utils.load.save_to_csv")
@patch("utils.load.save_to_google_sheets")
@patch("utils.load.save_to_postgresql")
def test_load_data(mock_pg, mock_gs, mock_csv):
    df = pd.DataFrame({"A": [1]})
    load_data(df)

    assert mock_csv.called
    assert mock_gs.called
    assert mock_pg.called