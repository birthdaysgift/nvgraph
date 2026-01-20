import collections


class AutoList(collections.UserList):
    def __init__(self, data=None, default=None):
        super().__init__(data or [])
        self._default = default

    def __setitem__(self, index, value):
        while index > len(self.data) - 1 :
            self.data.append(self._default)
        self.data[index] = value


def list_index(iterable, value, append=False, start=None):
    start = start or 0
    for i, v in enumerate(iterable[start:], start):
        if v == value:
            return i
    if append:
        iterable.append(value)
        return len(iterable) - 1


def find_dups(iterable, exclude=None):
    exclude = exclude or tuple()
    seen = []
    for i, value in enumerate(iterable):
        if value in exclude:
            continue
        if value in seen:
            yield value, i
            continue
        seen.append(value)


def replace(iterable, value, replacement):
    result = iterable.copy()
    for i, v in enumerate(iterable):
        if v == value:
            result[i] = replacement
    return result


def add_horizontal_connectors(connectors, start, stop):
    for i in range(start, stop):
        first_char = connectors[i][0]
        if first_char == " ":
            first_char = "─"
        connectors[i] = first_char + "─"

