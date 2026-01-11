import subprocess
import collections


class AutoList:
    def __init__(self, default=None):
        self._data = []
        self._default = default

    def put(self, index, value):
        while index > len(self._data) - 1 :
            self._data.append(self._default)
        self._data[index] = value

    def __repr__(self):
        return repr(self._data)

    def __iter__(self):
        return iter(self._data)


def main():
    commits, tree = parse(cmd("date", limit=50))
    lines = format(commits, tree)
    for line in lines:
        print(line)


def format(commits, tree):
    fallcommits = AutoList()
    for row, commit in enumerate(commits):
        col = tree[commit["hash"]]["col"]

        fallcommits.put(col, commit["hash"])
        shift = ""
        for fcol, fcommit in enumerate(fallcommits):
            if fcol == col:
                shift += "* "
                continue
            if fcommit is not None:
                shift += "│ "
                continue
            if fcommit is None:
                shift += "  "


        connectors = AutoList(default="  ")
        for parent in tree[commit["hash"]]["parents"]:
            parent_col = tree[parent]["col"]
            parent_row = tree[parent]["row"]

            for fcol, fcommit in enumerate(fallcommits):
                if fcommit is None:
                    connectors.put(fcol, "  ")
                if fcommit is not None:
                    connectors.put(fcol, "│ ")

            # parent is beyond chosen commit scope
            if parent_col is None:
                connectors.put(col, "│ ")
                fallcommits.put(col, "beyondscope")
                continue

            # child and parent are in the same column
            if parent_col == col:
                connectors.put(col, "│ ")
                fallcommits.put(col, parent)
                continue

            # branch is merged into current commit
            if parent_col > col:
                connectors.put(parent_col, "╮ ")
                fallcommits.put(parent_col, parent)
                for i, connector in enumerate(connectors):
                    if i == parent_col:
                        break
                    connectors.put(i, connector[0] + "─")
                continue

        for fcol, fcommit in enumerate(fallcommits):
            for fparent in tree[fcommit]["parents"]:
                if tree[fparent]["col"] is not None and tree[fparent]["col"] < fcol and tree[fparent]["row"] == row + 1:
                    connectors.put(fcol, "╯ ")
                    fallcommits.put(fcol, None)
                    for i, connector in enumerate(connectors):
                        if i == fcol:
                            break
                        connectors.put(i, connector[0] + "─")
                    continue

        yield commit["hash"] + "  " + shift
        yield (" " * len(commit["hash"])) + "  " + "".join(connectors)


def register_column(columns, hash, tree):
    for col, col_hash in enumerate(columns):
        if tree[col_hash]["parents"] and hash == tree[col_hash]["parents"][0]:
            # either RC or MC.left_parent
            return col
        if col_hash == f"occupied {hash}":
            # occupied before
            return col

    # choose leftmost available column (contains None)
    col = list_index(columns, None)
    if col is not None:
        return col
    columns.append(hash)
    return len(columns) - 1


def free_columns(columns: list, hash, tree):
    for child in tree[hash]["children"]:
        hash_index = list_index(columns, hash)
        child_index = list_index(columns, child)
        if child_index is not None and child_index != hash_index and tree[child]["parents"] == [hash]:
            columns[child_index] = None


def occupy_columns(columns: list, hash, tree):
    if len(tree[hash]["parents"]) == 2:
        # choose leftmost available column (contains None)
        right_parent = tree[hash]["parents"][1]
        col = list_index(columns, None)
        if col is not None:
            columns[col] = f"occupied {right_parent}"
            return col
        if col is None:
            columns.append(f"occupied {right_parent}")
            return len(columns) - 1


def list_index(iterable, value):
    for i, v in enumerate(iterable):
        if v == value:
            return i
    return None


def parse(text):
    commits = []
    tree = collections.defaultdict(lambda: {"parents": [], "children": [], "col": None, "row": None})

    columns = []  # currently occupied columns
    for row, line in enumerate(text.split(b"\n")):
        hash, parents, refs, subject, author = [v.decode() for v in line.split(b"^")]
        commits.append({"hash": hash, "refs": refs, "subject": subject, "author": author})

        for parent in parents.split(" "):
            tree[hash]["parents"].append(parent)
            tree[parent]["children"].append(hash)

        col = register_column(columns, hash, tree)
        columns[col] = hash
        tree[hash]["col"] = col
        tree[hash]["row"] = row
        free_columns(columns, hash, tree)
        occupy_columns(columns, hash, tree)

    return commits, tree


def cmd(order_type, limit):
    cmd = f'git log --all --pretty=format:%h^%p^%D^%s^%an --max-count={limit} --{order_type}-order'
    result = subprocess.run(cmd.split(" "), cwd="/home/mint/code/ip_api_test_graph", capture_output=True)
    return result.stdout.strip()


if __name__ == "__main__":
    main()
