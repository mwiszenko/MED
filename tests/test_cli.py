import argparse
import pytest

from med.cli import min_support_type


def test_min_support_type():
    assert min_support_type("1") == 1
    with pytest.raises(argparse.ArgumentTypeError):
        min_support_type("2")
    with pytest.raises(argparse.ArgumentTypeError):
        min_support_type("invalid")
