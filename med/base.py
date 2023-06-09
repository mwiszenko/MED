from __future__ import annotations

import copy

from tqdm import tqdm

MIN_SUPPORT_VAL = 0.0
MAX_SUPPORT_VAL = 1.0


class ItemSet:
    def __init__(self, items: list[str]):
        self.items: list[str] = items

    def __len__(self):
        return len(self.items)

    def __setitem__(self, item_number: int, data: str):
        self.items[item_number] = data

    def __getitem__(self, item_number: int):
        return self.items[item_number]

    def __delitem__(self, item_number: int):
        del self.items[item_number]

    def __str__(self):
        return "(" + " ".join(self.items) + ")"

    def __repr__(self):
        return self.__str__()

    def __contains__(self, key: str):
        return key in self.items

    def append(self, item: str):
        self.items.append(item)
        return self.items

    def is_subset(self, its: ItemSet):
        return set(self.items).issubset(its.items)


class Sequence:
    def __init__(self, item_sets: list[ItemSet]):
        self.item_sets: list[ItemSet] = item_sets

    def __len__(self):
        return len(self.item_sets)

    def __setitem__(self, item_set_number: int, data: ItemSet):
        self.item_sets[item_set_number] = data

    def __getitem__(self, item_set_number: int):
        return self.item_sets[item_set_number]

    def __delitem__(self, item_set_number: int):
        del self.item_sets[item_set_number]

    def __str__(self):
        return "(" + "".join(str(i) for i in self.item_sets) + ")"

    def __repr__(self):
        return self.__str__()

    def __contains__(self, key: str):
        return any(key in its for its in self.item_sets)

    def append(self, item_set: ItemSet):
        self.item_sets.append(item_set)
        return self

    def is_subset(self, seq: Sequence):
        ln, j = len(self), 0
        if ln > len(seq):
            return False, -1
        for idx, ele in enumerate(seq.item_sets):
            if self.item_sets[j].is_subset(ele):
                j += 1
            if j == ln:
                return True, idx
        return False, -1

    def extend_sequence(self, seq: Sequence):
        return seq


class DataSet:
    def __init__(self, sequences: list[Sequence]):
        self.sequences: list[Sequence] = sequences

    def __len__(self):
        return len(self.sequences)

    def __setitem__(self, sequence_number: int, data: Sequence):
        self.sequences[sequence_number] = data

    def __getitem__(self, sequence_number: int):
        return self.sequences[sequence_number]

    def __delitem__(self, sequence_number: int):
        del self.sequences[sequence_number]

    def __str__(self):
        return "\n".join(
            str(idx + 1) + ": " + str(i)
            for idx, i in enumerate(self.sequences)
        )

    def __repr__(self):
        return self.__str__()

    def __contains__(self, key: str):
        return any(key in seq for seq in self.sequences)

    def get_set(self):
        return sorted(
            set(
                [
                    item
                    for sublist in [
                        item.items
                        for sublist in self.sequences
                        for item in sublist
                    ]
                    for item in sublist
                ]
            )
        )

    def get_support(self, seq: Sequence):
        support: int = 0
        for s in self.sequences:
            is_subset, idx = seq.is_subset(s)
            if is_subset:
                support = support + 1
        return support

    def get_sequences(self, seq: Sequence):
        characters = self.get_set()
        sequences: list[Sequence] = []
        for c in characters:
            sequences.append(copy.deepcopy(seq).append(ItemSet([c])))
        return sequences


def read_sequence_file(filename: str):
    sequences: list[Sequence] = []

    try:
        with open(filename, "r", encoding="UTF-8") as file:
            while line := file.readline():
                item_sets: list[ItemSet] = []
                for its in line.strip().split(" "):
                    item_sets.append(ItemSet(its.split(":")))
                sequences.append(Sequence(item_sets))
    except FileNotFoundError:
        msg = filename + " does not exist."
        print(msg)
    return DataSet(sequences)


def project(ds: DataSet, seq: Sequence):
    sequences: list[Sequence] = []
    for s in ds.sequences:
        is_subset, idx = seq.is_subset(s)
        if is_subset:
            new_s = copy.deepcopy(s)
            new_s.item_sets = new_s.item_sets[idx + 1 :]
            sequences.append(new_s)
    return DataSet(sequences)


def prefix_span(ds: DataSet, min_sup: float):
    results: dict[Sequence, int] = {}
    prefix_span_rec(ds, Sequence(item_sets=[]), min_sup, results)
    return results


def prefix_span_rec(ds: DataSet, seq_s: Sequence, min_sup: float, results):
    sequences = ds.get_sequences(seq_s)
    for seq_r in sequences:
        c = Sequence([ItemSet([seq_r.item_sets[-1][0]])])
        sup_r = ds.get_support(c)
        if sup_r > min_sup:
            results[seq_r] = sup_r
            dr = project(ds, c)
            prefix_span_rec(dr, seq_r, min_sup, results)
