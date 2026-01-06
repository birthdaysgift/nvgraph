import subprocess
import collections


def main():
    log = cmd("topo")

    commits, tree = parse(log)
    for line in format(commits, tree):
        print(line)


def format(commits, tree):
    columns = []

    for commit in commits:
        hash = commit["hash"]

        # ALGO BEGIN
        free_columns(columns, hash, tree)
        col = register_column(columns, hash, tree)
        # ALGO END

        shift = " | " * col
        yield f"{shift} * {hash}"


def register_column(columns, hash, tree):
    for col, col_hash in enumerate(columns):

        if hash not in tree[col_hash]["parents"]:
            continue
        parents = tree[col_hash]["parents"]

        # either RC or MC.left_parent
        if hash == parents[0]:
            columns[col] = hash
            return col

    # choose leftmost available
    for col, col_hash in enumerate(columns):
        if col_hash is None:
            columns[col] = hash
            return col
    columns.append(hash)
    return len(columns) - 1


def free_columns(columns, hash, tree):
    for child in tree[hash]["children"]:
        for col, col_hash in enumerate(columns):
            if col_hash == child and tree[child]["parents"] == [hash]:
                columns[col] = None


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


def cmd(order_type):
    cmd = f'git log --all --pretty=format:%h^%p^%D^%s^%an --max-count=50 --{order_type}-order'
    result = subprocess.run(cmd.split(" "), text=False, cwd="/home/mint/code/ip_api", capture_output=True)
    return result.stdout.strip()


if __name__ == "__main__":
    main()
