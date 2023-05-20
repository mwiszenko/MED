MIN_SUPPORT_VAL = 0.0
MAX_SUPPORT_VAL = 1.0


class ItemSet:
    def __init__(self, items: list[str]):
        self.items: list[str] = items

    def __len__(self):
        return len(self.items)

    def __setitem__(self, item_number, data):
        self.items[item_number] = data

    def __getitem__(self, item_number):
        return self.items[item_number]

    def __str__(self):
        return str(self.items)

    def __repr__(self):
        return self.__str__()


class Sequence:
    def __init__(self, item_sets: list[ItemSet]):
        self.item_sets: list[ItemSet] = item_sets

    def __len__(self):
        return sum(len(i) for i in self.item_sets)

    def __setitem__(self, item_set_number, data):
        self.item_sets[item_set_number] = data

    def __getitem__(self, item_set_number):
        return self.item_sets[item_set_number]

    def __str__(self):
        return str(self.item_sets)

    def __repr__(self):
        return self.__str__()


class DataSet:
    def __init__(self, sequences: list[Sequence]):
        self.sequences: list[Sequence] = sequences

    def __len__(self):
        return len(self.sequences)

    def __setitem__(self, sequence_number, data):
        self.sequences[sequence_number] = data

    def __getitem__(self, sequence_number):
        return self.sequences[sequence_number]

    def __str__(self):
        return str(self.sequences)

    def __repr__(self):
        return self.__str__()


def read_sequence_file(filename: str):
    sequences: list[Sequence] = []

    try:
        with open(filename, "r", encoding="UTF-8") as file:
            while line := file.readline():
                item_sets: list[ItemSet] = []
                for i in line.strip().split(" "):
                    item_sets.append(ItemSet(i.split(":")))
                sequences.append(Sequence(item_sets))
    except FileNotFoundError:
        msg = filename + " does not exist."
        print(msg)
    return DataSet(sequences)
