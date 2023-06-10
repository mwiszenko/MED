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


def prefix_span(ds: DataSet, min_sup: float):
    results: dict[Sequence, int] = {}
    projection = dict.fromkeys(range(0, len(ds)), 0)
    prefix_span_rec(ds, projection, Sequence([]), min_sup, results)
    return results


def prefix_span_rec(ds: DataSet, proj: dict[int, int], seq_s: Sequence, min_sup: float, results):
    seq_to_sup: dict[Sequence, int] = get_sequences(ds, proj, seq_s)
    for seq_r, sup_r in seq_to_sup.items():
        if sup_r > min_sup:
            results[seq_r] = sup_r
            new_proj: dict[int, int] = project(ds, proj, seq_r)
            prefix_span_rec(ds, new_proj, seq_r, min_sup, results)


def project(ds: DataSet, proj: dict[int, int], seq_r: Sequence):
    new_proj: dict[int, int] = {}
    for idx, num in proj.items():
        new_num = get_place(seq_r, ds.sequences[idx])
        if new_num != -1:
            new_proj[idx] = new_num
    return new_proj


def get_sequences(ds: DataSet, proj: dict[int, int], seq: Sequence):
    # characters = ds.get_set(proj)
    characters = ds.get_set()
    seq_to_sup: dict[Sequence, int] = {}
    sequences: list[Sequence] = []
    for c in characters:
        sequences.append(copy.deepcopy(seq).append(ItemSet([c])))
    for s in sequences:
        seq_to_sup[s] = get_support(ds, proj, s)
    return seq_to_sup


def get_support(ds: DataSet, proj: dict[int, int], seq: Sequence):
    support: int = 0
    for idx, num in proj.items():
        is_contained = is_subset(seq, ds.sequences[idx])
        if is_contained:
            support = support + 1
    return support


def is_subset(smaller_seq: Sequence, bigger_seq: Sequence):
    ln, j = len(smaller_seq), 0
    for its in bigger_seq:
        if smaller_seq[j].is_subset(its):
            j += 1
        if j == ln:
            return True
    return False


def get_place(smaller_seq: Sequence, bigger_seq: Sequence):
    ln, j = len(smaller_seq), 0
    for idx, its in enumerate(bigger_seq.item_sets):
        if smaller_seq[j].is_subset(its):
            j += 1
        if j == ln:
            return idx
    return -1
