import pytest
import requests
from bs4 import BeautifulSoup
from unittest.mock import patch, Mock
from utils.extract import scrape_page, fetch_page, extract_all

HTML_SAMPLE = """
<div class="collection-card">
    <h3 class="product-title">Test Product</h3>
    <span class="price">$10</span>
    <p>4.5 / 5</p>
    <p>3 Colors</p>
    <p>Size: M</p>
    <p>Gender: Men</p>
</div>
"""

def test_scrape_page_valid():
    soup = BeautifulSoup(HTML_SAMPLE, "html.parser")
    results = scrape_page(soup)

    assert len(results) == 1
    assert results[0]["Title"] == "Test Product"
    assert results[0]["Price"] == "$10"
    assert results[0]["Rating"] == "4.5 / 5"
    assert results[0]["Colors"] == "3 Colors"
    assert results[0]["Size"] == "Size: M"
    assert results[0]["Gender"] == "Gender: Men"

@patch("utils.extract.requests.get")
def test_fetch_page_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "<html></html>"
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    soup = fetch_page("http://test.com")
    assert soup is not None

@patch("utils.extract.requests.get")
def test_fetch_page_error(mock_get):
    mock_get.side_effect = requests.RequestException("Error")
    soup = fetch_page("http://test.com")
    assert soup is None

@patch("utils.extract.fetch_page")
@patch("utils.extract.scrape_page")
def test_extract_all(mock_scrape, mock_fetch):
    mock_fetch.return_value = Mock()
    mock_scrape.return_value = [{"Title": "Test"}]

    df = extract_all(pages=2)
    assert len(df) == 2