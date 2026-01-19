import collections

from src.utils import AutoList, find_dups, list_index, replace, add_horizontal_connectors

def format(lines, tree):
    prev_connector_columns = []
    for row, (hash, connector_columns) in enumerate(lines):
        commit_symbols = AutoList(default="  ")

        prev_connector_columns = replace(prev_connector_columns, hash, None)
        for con_col, con_hash in enumerate(prev_connector_columns):
            if con_hash is not None:
                commit_symbols[con_col] = "│ "
        commit_symbols[tree[hash].col] = "* "

        yield hash + "  " + "".join(commit_symbols)


        connectors = AutoList(default="  ")

        # place straight connectors
        for con_col, con_hash in enumerate(connector_columns):
            if con_hash is not None:
                connectors[con_col] = "│ "

        # place merge connectors
        if tree[hash].parents.right is not None:
            new_br_col = list_index(connector_columns, tree[hash].parents.right)
            # merge from right col to left col
            if new_br_col is not None and new_br_col > tree[hash].col:
                connectors[new_br_col] = "╮ "
                add_horizontal_connectors(connectors, tree[hash].col, new_br_col)
            # merge from left col to right col
            if new_br_col is not None and new_br_col < tree[hash].col:
                connectors[new_br_col] = "╭ "
                add_horizontal_connectors(connectors, new_br_col, tree[hash].col)

        # place branchoff connectors
        branch_offs = find_dups(connector_columns, exclude=[None])
        for branchoff_hash, c in branch_offs:
            branchoff_row = tree[branchoff_hash].row
            if branchoff_row is not None and branchoff_row == row + 1:
                connectors[c] = "╯" + connectors[c][1]
                add_horizontal_connectors(connectors, tree[branchoff_hash].col, c)

        yield (" " * len(hash)) + "  " + "".join(connectors)

        prev_connector_columns = connector_columns.copy()


def get_column(columns, hash):
    for col, col_hash in enumerate(columns):
        if col_hash == hash:
            return col  # found column that was occupied before
    # or choose leftmost available column (contains None)
    return list_index(columns, None, append=True)


def define_columns(commits, tree):
    lines = []
    columns = []  # represents commits per column after current commit line
    for hash in commits:
        # define column for current commit
        col = get_column(columns, hash)
        tree[hash].col = col

        # register left parent of current commit to columns
        columns[col] = tree[hash].parents.left
        # free columns that should be merged to current hash
        columns = replace(columns, hash, None)
        # occupy column for right parent
        if tree[hash].parents.right is not None:
            col = get_column(columns, tree[hash].parents.right)
            columns[col] = tree[hash].parents.right

        lines.append((hash, columns.copy()))

    return lines, tree

