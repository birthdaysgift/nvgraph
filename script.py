import subprocess
import collections


def main():
    commits, tree = parse(cmd("topo", limit=100))
    lines = format(commits, tree)
    for line in lines:
        print(line)


def format(commits, tree):
    for commit in commits:
        yield commit + "  " + ("  " * tree[commit]["col"]) + "* "


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
    # TODO: occcupy columns for virtual parents whith are beyond current commit scope
    # (it's probably already done - check topo order) and then draw lines for these parents

    if len(tree[hash]["parents"]) == 2:

        right_parent = tree[hash]["parents"][1]
        # if right parent has two child - it means that branch have been merged
        # and then continued with another commit to that branch
        # in this case we won't occupy a new column, so it should be placed under its child
        if len(tree[right_parent]["children"]) > 1:
            return

        current_col = list_index(columns, hash)
        # after current column, find first available column (contains None) to place right parent there
        col = list_index(columns[current_col:], None)
        if col is not None:
            columns[col] = right_parent
            tree[right_parent]["col"] = col
        if col is None:
            columns.append(right_parent)
            tree[right_parent]["col"] = len(columns) - 1


def list_index(iterable, value):
    for i, v in enumerate(iterable):
        if v == value:
            return i
    return None


def parse(text):
    commits = []
    tree = collections.defaultdict(lambda: {"parents": [], "children": [], "col": None})

    columns = []  # currently occupied columns
    for line in text.split(b"\n"):
        hash, parents = [v.decode() for v in line.split(b"^")][:2]
        commits.append(hash)

        for parent in parents.split(" "):
            tree[hash]["parents"].append(parent)
            tree[parent]["children"].append(hash)

        col = register_column(columns, hash, tree)
        columns[col] = hash
        free_columns(columns, hash, tree)
        occupy_columns(columns, hash, tree)

        tree[hash]["col"] = col

    return commits, tree


def cmd(order_type, limit):
    cmd = f'git log --all --pretty=format:%h^%p^%D^%s^%an --max-count={limit} --{order_type}-order'
    result = subprocess.run(cmd.split(" "), cwd="/home/mint/code/ip_api_test_graph", capture_output=True)
    return result.stdout.strip()


if __name__ == "__main__":
    main()
