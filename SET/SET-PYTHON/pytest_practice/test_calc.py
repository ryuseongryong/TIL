import pytest
from lib_calc import add, substract, division, multiply


@pytest.fixture
def ten():
    return 10


def test_add(ten):
    assert add(ten, 20) == 30


def test_subtract(ten):
    assert substract(20, ten) == 10


def test_division(ten):
    assert division(20, ten) == 2


def test_multiply(ten):
    assert multiply(ten, 20) == 200
