import argparse

from med.base import DataSet, ItemSet, Sequence, prefix_span

MIN_PROBABILITY_FLOAT = 0.0
MAX_PROBABILITY_FLOAT = 1.0

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


def positive_int(arg: str):
    try:
        i = int(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Must be an integer number")
    if i < 0:
        raise argparse.ArgumentTypeError("Argument must be >= 0")
    return i


def probability_float(arg: str):
    try:
        f = float(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Must be a floating point number")
    if f < MIN_PROBABILITY_FLOAT or f > MAX_PROBABILITY_FLOAT:
        raise argparse.ArgumentTypeError(
            "Argument must be <= "
            + str(MAX_PROBABILITY_FLOAT)
            + " and >= "
            + str(MIN_PROBABILITY_FLOAT)
        )
    return f


def main():  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True)
    support = parser.add_mutually_exclusive_group(required=True)
    support.add_argument("--min_sup", type=positive_int)
    support.add_argument("--min_sup_percentage", type=probability_float)
    args = parser.parse_args()

    # ds: DataSet = read_sequence_file(filename=args.input)
    ds: DataSet = EXAMPLE_DATASET

    min_sup: float
    if args.min_sup is not None:
        min_sup = args.min_sup
    else:
        min_sup = args.min_sup_percentage * len(ds)
    res = prefix_span(ds, min_sup)
    print(res)
    print(len(res))
