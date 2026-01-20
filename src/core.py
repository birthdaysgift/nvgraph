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
                connectors[new_br_col] = "╮" + connectors[new_br_col][1]
                add_horizontal_connectors(connectors, tree[hash].col, new_br_col)
            # merge from left col to right col
            if new_br_col is not None and new_br_col < tree[hash].col:
                connectors[new_br_col] = "╭" + connectors[new_br_col][1]
                add_horizontal_connectors(connectors, new_br_col, tree[hash].col)

        # place fork connectors
        forks = find_dups(connector_columns, exclude=[None])
        for fork_hash, fork_col in forks:
            if tree[fork_hash].row == row + 1:
                # fork from left to right
                if fork_col > tree[fork_hash].col:
                    connectors[fork_col] = "╯" + connectors[fork_col][1]
                    add_horizontal_connectors(connectors, tree[fork_hash].col, fork_col)
                # fork from right to left
                if fork_col < tree[fork_hash].col:
                    connectors[fork_col] = "╰" + connectors[fork_col][1]
                    add_horizontal_connectors(connectors, fork_col, tree[fork_hash].col)

        yield (" " * len(hash)) + "  " + "".join(connectors)

        prev_connector_columns = connector_columns.copy()


def get_column(columns, hash, start=None):
    start = start or 0
    for col, col_hash in enumerate(columns[start:], start):
        if col_hash == hash:
            return col  # found column that was occupied before
    for col, col_hash in enumerate(columns[:start]):
        if col_hash == hash:
            return col  # found column that was occupied before
    # or choose leftmost available column (contains None)
    return list_index(columns, None, append=True, start=start)


def define_columns(commits, tree):
    lines = []
    columns = AutoList(default=None)  # represents commits per column after current commit line
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
            col = get_column(columns, tree[hash].parents.right, start=col)
            columns[col] = tree[hash].parents.right

        lines.append((hash, columns.copy()))

    return lines, tree

