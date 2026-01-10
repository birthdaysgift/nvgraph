import subprocess
import collections
from itertools import zip_longest


def main():
    commits, tree = parse(cmd("date", limit=50))
    lines = format(commits, tree)
    for line in lines:
        print(line)


def format(commits, tree):
    max_width = 0
    columns = []

    for commit in commits:

        if commit["hash"] == "9032e8e1":
            pass
        col = register_column(columns, commit["hash"], tree)
        columns[col] = commit["hash"]
        free_columns(columns, commit["hash"], tree)
        occupy_columns(columns, commit["hash"], tree)

        shift = ("| " * col) + "* "
        max_width = max(len(shift) + 3, max_width)

        yield shift + commit['hash']


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
    tree = collections.defaultdict(lambda: {"parents": [], "children": []})

    for line in text.split(b"\n"):
        hash, parents, refs, subject, author = [v.decode() for v in line.split(b"^")]
        commits.append({"hash": hash, "refs": refs, "subject": subject, "author": author})

        for parent in parents.split(" "):
            tree[hash]["parents"].append(parent)
            tree[parent]["children"].append(hash)

    return commits, tree


def cmd(order_type, limit):
    cmd = f'git log --all --pretty=format:%h^%p^%D^%s^%an --max-count={limit} --{order_type}-order'
    result = subprocess.run(cmd.split(" "), cwd="/home/mint/code/ip_api_test_graph", capture_output=True)
    return result.stdout.strip()


if __name__ == "__main__":
    main()
