def list_index(iterable, value, append=False):
    for i, v in enumerate(iterable):
        if v == value:
            return i
    if append:
        iterable.append(value)
        return len(iterable) - 1

