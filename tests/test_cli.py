import argparse
import pytest

from med.cli import min_support_type, min_support_percentage_type


def test_min_support_type():
    assert min_support_type("2") == 2
    with pytest.raises(argparse.ArgumentTypeError):
        min_support_type("-2")
    with pytest.raises(argparse.ArgumentTypeError):
        min_support_type("0.5")
    with pytest.raises(argparse.ArgumentTypeError):
        min_support_type("invalid")


def test_min_support_percentage_type():
    assert min_support_percentage_type("0.5") == 0.5
    with pytest.raises(argparse.ArgumentTypeError):
        min_support_percentage_type("2")
    with pytest.raises(argparse.ArgumentTypeError):
        min_support_percentage_type("invalid")
