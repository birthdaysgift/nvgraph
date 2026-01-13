import subprocess
import collections


def main():
    commits_data = cmd("topo", limit=100)
    commits, tree = parse_tree(commits_data)
    lines = format(commits, tree)
    for line in lines:
        print(line)


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


def list_index(iterable, value, append=False):
    for i, v in enumerate(iterable):
        if v == value:
            return i
    if append:
        iterable.append(value)
        return len(iterable) - 1


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


def cmd(order_type, limit):
    cmd = f'git log --all --pretty=format:%h^%p^%D^%s^%an --max-count={limit} --{order_type}-order'
    result = subprocess.run(cmd.split(" "), cwd="/home/mint/code/ip_api_test_graph", capture_output=True)
    for line in result.stdout.strip().split(b"\n"):
        hash, parents = [v.decode() for v in line.split(b"^")][:2]
        yield hash, parents.split(" ")


if __name__ == "__main__":
    main()
