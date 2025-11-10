# tests/test_utils.py
from src.utils import sanitize_price

def test_sanitize_price_basic():
    assert sanitize_price("R$ 1.234,56") == 1234.56
    assert sanitize_price("1.234,56") == 1234.56
    assert sanitize_price("1,234") == 1.234
    assert sanitize_price("999") == 999.0
    assert sanitize_price(None) is None
