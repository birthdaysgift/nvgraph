import collections


class AutoList(collections.UserList):
    def __init__(self, data=None, default=None):
        super().__init__(data or [])
        self._default = default

    def __setitem__(self, index, value):
        while index > len(self.data) - 1 :
            self.data.append(self._default)
        self.data[index] = value


def list_index(iterable, value, append=False):
    for i, v in enumerate(iterable):
        if v == value:
            return i
    if append:
        iterable.append(value)
        return len(iterable) - 1


def find_dups(iterable, exclude=None):
    exclude = exclude or tuple()
    result = collections.defaultdict(list)
    seen = []
    for i, value in enumerate(iterable):
        if value in exclude:
            continue
        if value in seen:
            result[value].append(i)
            continue
        seen.append(value)
    return result
