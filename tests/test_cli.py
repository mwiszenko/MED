import argparse
import pytest

from med.cli import (
    non_negative_int,
    probability_float,
    MIN_PROBABILITY_FLOAT,
    MAX_PROBABILITY_FLOAT,
)


def test_constants():
    assert MIN_PROBABILITY_FLOAT == 0.0
    assert MAX_PROBABILITY_FLOAT == 1.0


def test_positive_int():
    assert non_negative_int("2") == 2
    with pytest.raises(argparse.ArgumentTypeError):
        non_negative_int("-2")
    with pytest.raises(argparse.ArgumentTypeError):
        non_negative_int("0.5")
    with pytest.raises(argparse.ArgumentTypeError):
        non_negative_int("invalid")


def test_min_support_percentage_type():
    assert probability_float("0.5") == 0.5
    with pytest.raises(argparse.ArgumentTypeError):
        probability_float("2")
    with pytest.raises(argparse.ArgumentTypeError):
        probability_float("invalid")
