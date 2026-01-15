import collections

from src.utils import AutoList, find_dups, list_index, replace


def format(lines, tree):
    prev_connector_columns = []
    for row, (hash, connector_columns) in enumerate(lines):
        commit_symbols = AutoList(default="  ")

        prev_connector_columns = replace(prev_connector_columns, hash, None)
        for con_col, con_hash in enumerate(prev_connector_columns):
            if con_hash is not None:
                commit_symbols[con_col] = "│ "
        commit_symbols[tree[hash]["col"]] = "* "

        yield hash + "  " + "".join(commit_symbols)


        connectors = AutoList(default="  ")

        # place straight connectors
        for con_col, con_hash in enumerate(connector_columns):
            if con_hash is not None:
                connectors[con_col] = "│ "

        # place merge connectors
        if len(tree[hash]["parents"]) == 2:
            new_br_col = list_index(connector_columns, tree[hash]["parents"][1])
            # merge from right col to left col
            if new_br_col is not None and new_br_col > tree[hash]["col"]:
                connectors[new_br_col] = "╮ "
                # add horizontal connectors
                for i in range(tree[hash]["col"], new_br_col):
                    first_char = connectors[i][0]
                    if first_char == " ":
                        first_char = "─"
                    connectors[i] = first_char + "─"
            # merge from left col to right col
            if new_br_col is not None and new_br_col < tree[hash]["col"]:
                connectors[new_br_col] = "╭ "
                # add horizontal connectors
                for i in range(new_br_col, tree[hash]["col"]):
                    first_char = connectors[i][0]
                    if first_char == " ":
                        first_char = "─"
                    connectors[i] = first_char + "─"

        # place branchoff connectors
        branch_offs = find_dups(connector_columns, exclude=[None])
        for branchoff_hash, branchoff_cols in branch_offs.items():
            branchoff_row = tree[branchoff_hash]["row"]
            if branchoff_row is not None and branchoff_row == row + 1:
                for c in branchoff_cols:
                    connectors[c] = "╯" + connectors[c][1]
                # add horizontal connectors
                for c in branchoff_cols:
                    for i in range(tree[branchoff_hash]["col"], c):
                        first_char = connectors[i][0]
                        if first_char == " ":
                            first_char = "─"
                        connectors[i] = first_char + "─"

        yield (" " * len(hash)) + "  " + "".join(connectors)

        prev_connector_columns = connector_columns.copy()


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

