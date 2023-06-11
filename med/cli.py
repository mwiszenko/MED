import argparse

from med.base import (
    MAX_SUPPORT_VAL,
    MIN_SUPPORT_VAL,
    DataSet,
    ItemSet,
    Sequence,
    prefix_span,
)

ITS1_1 = ItemSet(["1"])
ITS1_2 = ItemSet(["1", "2", "3"])
ITS1_3 = ItemSet(["1", "3"])
ITS1_4 = ItemSet(["4"])
ITS1_5 = ItemSet(["3", "6"])
SEQ1 = Sequence([ITS1_1, ITS1_2, ITS1_3, ITS1_4, ITS1_5])

ITS2_1 = ItemSet(["1", "4"])
ITS2_2 = ItemSet(["3"])
ITS2_3 = ItemSet(["2", "3"])
ITS2_4 = ItemSet(["1", "5"])
SEQ2 = Sequence([ITS2_1, ITS2_2, ITS2_3, ITS2_4])

ITS3_1 = ItemSet(["5", "6"])
ITS3_2 = ItemSet(["1", "2"])
ITS3_3 = ItemSet(["4", "6"])
ITS3_4 = ItemSet(["3"])
ITS3_5 = ItemSet(["2"])
SEQ3 = Sequence([ITS3_1, ITS3_2, ITS3_3, ITS3_4, ITS3_5])

ITS4_1 = ItemSet(["5"])
ITS4_2 = ItemSet(["7"])
ITS4_3 = ItemSet(["1", "6"])
ITS4_4 = ItemSet(["3"])
ITS4_5 = ItemSet(["2"])
ITS4_6 = ItemSet(["3"])
SEQ4 = Sequence([ITS4_1, ITS4_2, ITS4_3, ITS4_4, ITS4_5, ITS4_6])

EXAMPLE_DATASET = DataSet([SEQ1, SEQ2, SEQ3, SEQ4])


def min_support_type(arg: str):
    try:
        i = int(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Must be an integer number")
    if i < 0:
        raise argparse.ArgumentTypeError("Argument must be >= 0")
    return i


def min_support_percentage_type(arg: str):
    try:
        f = float(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Must be a floating point number")
    if f < MIN_SUPPORT_VAL or f > MAX_SUPPORT_VAL:
        raise argparse.ArgumentTypeError(
            "Argument must be <= "
            + str(MAX_SUPPORT_VAL)
            + " and >= "
            + str(MIN_SUPPORT_VAL)
        )
    return f


def main():  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True)
    support = parser.add_mutually_exclusive_group(required=True)
    support.add_argument("--min-sup", type=min_support_type)
    support.add_argument("--min-sup-percentage", type=min_support_percentage_type)
    args = parser.parse_args()

    # ds: DataSet = read_sequence_file(filename=args.input)
    ds: DataSet = EXAMPLE_DATASET

    min_sup: float
    if args.minSup is not None:
        min_sup = args.minSup
    else:
        min_sup = args.minSupPercentage * len(ds)
    res = prefix_span(ds, min_sup)
    print(res)
    print(len(res))
