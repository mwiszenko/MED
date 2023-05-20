import pytest

from med.base import (
    MIN_SUPPORT_VAL,
    MAX_SUPPORT_VAL,
    ItemSet,
    Sequence,
    DataSet,
    read_sequence_file,
)


def test_constants():
    assert MIN_SUPPORT_VAL == 0.0
    assert MAX_SUPPORT_VAL == 1.0


def test_item_set():
    items: list[str] = ["0", "1"]
    its: ItemSet = ItemSet(items)
    assert type(its) == ItemSet
    assert its.items == items
    assert len(its) == 2
    assert str(its) == str(items) == repr(its)
    its[0] = "2"
    assert its[0] == "2"


def test_sequence():
    items: list[str] = ["0", "1"]
    item_sets: list[ItemSet] = [ItemSet(items), ItemSet(items)]
    seq: Sequence = Sequence(item_sets)
    assert type(seq) == Sequence
    assert seq.item_sets == item_sets
    assert len(seq) == sum(len(i) for i in item_sets)
    assert str(seq) == str(item_sets) == repr(seq)
    seq[0] = ItemSet(["2"])
    assert seq[0][0] == "2"


def test_data_set():
    items: list[str] = ["0", "1"]
    item_sets: list[ItemSet] = [ItemSet(items), ItemSet(items)]
    sequences: list[Sequence] = [Sequence(item_sets), Sequence(item_sets)]
    ds: DataSet = DataSet(sequences)
    assert type(ds) == DataSet
    assert ds.sequences == sequences
    assert len(ds) == len(sequences)
    assert str(ds) == str(sequences) == repr(ds)
    ds[0] = Sequence([ItemSet(["2"])])
    assert ds[0][0][0] == "2"


TEST_DATA = [
    [read_sequence_file(filename="tests/data/test.txt"), 4],
    [read_sequence_file(filename="invalid"), 0],
]


@pytest.mark.parametrize("data_set,length", TEST_DATA)
def test_read_sequence_file_2(data_set: DataSet, length: int):
    assert type(data_set) == DataSet
    assert len(data_set) == length
