import subprocess
import collections


class AutoList(collections.UserList):
    def __init__(self, data=None, default=None):
        super().__init__(data or [])
        self._default = default

    def put(self, index, value):
        while index > len(self.data) - 1 :
            self.data.append(self._default)
        self.data[index] = value


def main():
    commits, tree = parse(cmd("date", limit=50))
    lines = format(commits, tree)
    for line in lines:
        print(line)


def format(commits, tree):
    fallcommits = AutoList()
    for row, commit in enumerate(commits):
        col = tree[commit["hash"]]["col"]

        # generate commit line
        shift = AutoList(default="  ")
        [shift.put(fcol, "│ ") for fcol, fcommit in enumerate(fallcommits) if fcommit is not None]
        shift.put(col, "* ")
        yield commit["hash"] + "  " + "".join(shift)

        # generate connector line below the commit line
        connectors = AutoList(default="  ")
        [connectors.put(fcol, "│ ") for fcol, fcommit in enumerate(fallcommits) if fcommit is not None]
        for parent in tree[commit["hash"]]["parents"]:
            parent_col = tree[parent]["col"]
            # parent is beyond chosen commit scope or child and parent are in the same column
            if parent_col is None or parent_col == col:
                connectors.put(col, "│ ")
                fallcommits.put(col, parent)
                continue
            # branch is merged into current commit
            if parent_col > col:
                connectors.put(parent_col, "╮ ")
                fallcommits.put(parent_col, parent)
                for i, connector in enumerate(connectors[:parent_col]):
                    connectors.put(i, "──" if connector == "  " else connector[0] + "─")
        for fcol, fcommit in enumerate(fallcommits):
            for fparent in tree[fcommit]["parents"]:
                if tree[fparent]["col"] is not None and tree[fparent]["col"] < fcol and tree[fparent]["row"] == row + 1:
                    connectors.put(fcol, "╯ ")
                    fallcommits.put(fcol, None)
                    for i, connector in enumerate(connectors[:fcol]):
                        connectors.put(i, "──" if connector == "  " else connector[0] + "─")
        yield (" " * len(commit["hash"])) + "  " + "".join(connectors)


def register_column(columns, hash, tree):
    for col, col_hash in enumerate(columns):
        if tree[col_hash]["parents"] and hash == tree[col_hash]["parents"][0]:
            # either RC or MC.left_parent
            return col
        if col_hash == hash:
            # occupied before
            return col

    # choose leftmost available column (contains None)
    col = list_index(columns, None)
    if col is not None:
        return col
    columns.append(None)
    return len(columns) - 1


def free_columns(columns: list, hash, tree):
    for child in tree[hash]["children"]:
        hash_index = list_index(columns, hash)
        child_index = list_index(columns, child)
        if child_index is not None and child_index != hash_index and tree[child]["parents"] == [hash]:
            columns[child_index] = None


def occupy_columns(columns: list, hash, tree):
    if len(tree[hash]["parents"]) == 2:
        # choose leftmost available column (contains None) to place right parent there
        right_parent = tree[hash]["parents"][1]
        # if right parent has two child - it means that branch have been merged
        # and then continued with another commit to that branch
        # in this case we won't occupy a new column, so it should be placed under its child
        if len(tree[right_parent]["children"]) > 1:
            return

        col = list_index(columns, None)
        if col is not None:
            columns[col] = right_parent
        if col is None:
            columns.append(right_parent)


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
        free_columns(columns, hash, tree)
        occupy_columns(columns, hash, tree)

        tree[hash]["col"] = col
        tree[hash]["row"] = row

    return commits, tree


def cmd(order_type, limit):
    cmd = f'git log --all --pretty=format:%h^%p^%D^%s^%an --max-count={limit} --{order_type}-order'
    result = subprocess.run(cmd.split(" "), cwd="/home/mint/code/ip_api_test_graph", capture_output=True)
    return result.stdout.strip()


if __name__ == "__main__":
    main()
