import argparse
from time import time

from med.base import DataSet, ItemSet, Sequence, prefix_span, read_sequence_file
from med.constants import (
    DEFAULT_MAX_LENGTH,
    DEFAULT_MIN_LENGTH,
    MAX_PROBABILITY_FLOAT,
    MIN_PROBABILITY_FLOAT,
)


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
