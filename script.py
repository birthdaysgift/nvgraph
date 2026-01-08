import subprocess
import collections


def main():
    commits, tree = parse(cmd("topo", limit=50))
    for line in format(commits, tree):
        print(line)


def format(commits, tree):
    columns = []

    for commit in commits:
        free_columns(columns, commit["hash"], tree)
        col = register_column(columns, commit["hash"], tree)
        columns[col] = commit["hash"]

        shift = "   " * col
        yield f"{shift} * {commit['hash']}"


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
