import collections

from src.utils import AutoList, find_dups, list_index


def format(lines, tree):
    for row, (hash, connector_columns) in enumerate(lines):

        connectors = AutoList(default="  ")

        # place merge connectors
        if len(tree[hash]["parents"]) == 2:
            new_br_col = list_index(connector_columns, tree[hash]["parents"][1])
            if new_br_col is not None:
                connectors[new_br_col] = "╮ "

        # place branchoff connectors
        branch_offs = find_dups(connector_columns, exclude=[None])
        for branchoff_hash, branchoff_cols in branch_offs.items():
            branchoff_row = tree[branchoff_hash]["row"]
            if branchoff_row is not None and branchoff_row == row + 1:
                for c in branchoff_cols:
                    connectors[c] = "╯ "


        yield hash + "  " + ("  " * tree[hash]["col"]) + "* "
        yield (" " * len(hash)) + "  " + "".join(connectors)

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
    tree = collections.defaultdict(lambda: {"parents": [], "children": [], "col": None, "row": None})

    columns = []  # represents commits per column after current commit line
    for row, (hash, parents) in enumerate(commits_data):

        for parent in parents:
            tree[hash]["parents"].append(parent)
            tree[parent]["children"].append(hash)

        # define column for current commit
        col = get_column(columns, hash)
        tree[hash]["col"] = col
        tree[hash]["row"] = row

        # register left parent of current commit to columns
        columns[col] = tree[hash]["parents"][0]
        # free columns that should be merged to current hash
        free_columns(columns, hash)
        # occupy column for right parent
        if len(tree[hash]["parents"]) > 1:
            right_parent = tree[hash]["parents"][1]
            col = get_column(columns, right_parent)
            columns[col] = right_parent

        commits.append((hash, columns.copy()))

    return commits, tree

