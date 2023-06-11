import argparse
from time import time

from med.base import DataSet, ItemSet, Sequence, prefix_span, read_sequence_file
from med.constants import (
    DEFAULT_MAX_LENGTH,
    DEFAULT_MIN_LENGTH,
    MAX_PROBABILITY_FLOAT,
    MIN_PROBABILITY_FLOAT,
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


def non_negative_int(arg: str):
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
    parser.add_argument("--output", "-o", type=str)
    parser.add_argument(
        "--max_length", type=non_negative_int, default=DEFAULT_MAX_LENGTH
    )
    parser.add_argument(
        "--min_length", type=non_negative_int, default=DEFAULT_MIN_LENGTH
    )
    support = parser.add_mutually_exclusive_group(required=True)
    support.add_argument("--min_sup", type=non_negative_int)
    support.add_argument("--min_sup_percentage", type=probability_float)
    args = parser.parse_args()

    ds: DataSet = read_sequence_file(filename=args.input)
    # ds: DataSet = EXAMPLE_DATASET

    min_sup: float
    if args.min_sup is not None:
        min_sup = args.min_sup
    else:
        min_sup = args.min_sup_percentage * len(ds)
    start_time = time()
    res: dict[Sequence, int] = prefix_span(
        ds, min_sup, args.min_length, args.max_length
    )
    print("--- %s seconds ---" % (time() - start_time))
    ordered_res: dict[Sequence, int] = dict(
        sorted(res.items(), key=lambda item: item[1], reverse=True)
    )
    number_of_found_sequences: str = "Number of found sequences: " + str(
        len(ordered_res)
    )
    found_sequences: str = "\n".join(
        "{}: {}".format(k, v) for k, v in ordered_res.items()
    )
    if args.output:
        with open(args.output, "w") as output:
            output.write(str(args))
            output.write("\n\n")
            output.write(number_of_found_sequences)
            output.write("\n\n")
            output.write(found_sequences)
    else:
        print(number_of_found_sequences)
        print(found_sequences)
