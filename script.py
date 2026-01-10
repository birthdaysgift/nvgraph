import subprocess
import collections
from itertools import zip_longest


def main():
    commits, tree = parse(cmd("topo", limit=50))
    width, lines = format(commits, tree)
    for graph_line, message in lines:
        print(f"{graph_line.ljust(width, ' ')}{message}")


def format(commits, tree):
    max_width = 0
    columns = []

    result = []

    for commit in commits:
        prev_columns = columns.copy()

        free_columns(columns, commit["hash"], tree)
        col = register_column(columns, commit["hash"], tree)
        columns[col] = commit["hash"]

        connectors = ["   " for _ in columns]
        for i, column_hash in enumerate(prev_columns):

            # branch start connector
            if column_hash in tree[commit["hash"]]["children"]:
                child_col = list_index(prev_columns, column_hash)
                if child_col > col:
                    connectors[child_col] = " ╯ "

            # branch merge connector
            if column_hash in tree[commit["hash"]]["children"]:
                child = column_hash
                if len(tree[child]["parents"]) == 2 and commit["hash"] == tree[child]["parents"][1]:
                    if child_col < col:
                        connectors[col] = " ╮ "

            if None not in (columns[i], column_hash):
                connectors[i] = " │ "

        result.append(("".join(connectors), ""))

        commit_line = []
        for prev_col, curr_col in zip_longest(prev_columns, columns, fillvalue=None):
            if curr_col == commit["hash"]:
                commit_line.append(" * ")
                continue
            if prev_col and curr_col:
                commit_line.append(" │ ")
                continue
            commit_line.append("   ")

        shift = "".join(commit_line)
        max_width = max(len(shift) + 3, max_width)

        result.append((shift, commit['hash']))

    return max_width, result


def register_column(columns, hash, tree):
    for col, col_hash in enumerate(columns):
        if tree[col_hash]["parents"] and hash == tree[col_hash]["parents"][0]:
            # either RC or MC.left_parent
            return col

    # choose leftmost available column (contains None)
    col = list_index(columns, None)
    if col is not None:
        return col
    columns.append(hash)
    return len(columns) - 1


def free_columns(columns: list, hash, tree):
    for child in tree[hash]["children"]:
        col = list_index(columns, child)
        if col is not None and tree[child]["parents"] == [hash]:
            columns[col] = None


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
