import argparse
import pandas as pd

from med.base import MIN_SUPPORT_VAL, MAX_SUPPORT_VAL


def min_support_type(arg: str):
    try:
        f = float(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Must be a floating point number")
    if f < MIN_SUPPORT_VAL or f > MAX_SUPPORT_VAL:
        raise argparse.ArgumentTypeError(
            "Argument must be < " + str(MAX_SUPPORT_VAL) + " and > " + str(MIN_SUPPORT_VAL))
    return f


def main():  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, required=True)
    parser.add_argument('--minSup', '-ms', type=min_support_type, required=True)
    args = parser.parse_args()
