import collections

from src.utils import list_index


def format(commits, tree):
    for commit in commits:
        yield commit + "  " + ("  " * tree[commit]["col"]) + "* "


def get_column(columns, hash):
    for col, col_hash in enumerate(columns):
        if col_hash == hash:
            return col  # found column that was occupied before
    # or choose leftmost available column (contains None)
    return list_index(columns, None, append=True)


def free_columns(columns: list, hash):
    for col, col_hash in enumerate(columns):
        if col_hash == hash:
            columns[col] = None


def parse_tree(commits_data):
    commits = []
    tree = collections.defaultdict(lambda: {"parents": [], "children": [], "col": None})

    columns = []  # represents commits per column after current commit line
    for hash, parents in commits_data:
        commits.append(hash)

        for parent in parents:
            tree[hash]["parents"].append(parent)
            tree[parent]["children"].append(hash)

        # define column for current commit
        col = get_column(columns, hash)
        tree[hash]["col"] = col

        # register left parent of current commit to columns
        columns[col] = tree[hash]["parents"][0]
        # free columns that should be merged to current hash
        free_columns(columns, hash)
        # occupy column for right parent
        if len(tree[hash]["parents"]) > 1:
            right_parent = tree[hash]["parents"][1]
            col = get_column(columns, right_parent)
            columns[col] = right_parent

    return commits, tree

