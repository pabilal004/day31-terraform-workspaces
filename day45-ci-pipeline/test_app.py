import pytest
from app import calculate_total


def test_calculate_total():
    assert calculate_total(10, 3) == 30


def test_negative_price():
    with pytest.raises(ValueError):
        calculate_total(-10, 3)


def test_negative_quantity():
    with pytest.raises(ValueError):
        calculate_total(10, -3)
