import collections
import subprocess


def cmd(order_type, limit):
    cmd = f'git log --all --pretty=format:%h^%p^%D^%s^%an --max-count={limit} --{order_type}-order'
    result = subprocess.run(cmd.split(" "), cwd="/home/mint/code/ip_api_test_graph", capture_output=True)

    commits = []
    tree = collections.defaultdict(lambda: {"parents": [], "col": None, "row": None})
    for row, line in enumerate(result.stdout.strip().split(b"\n")):
        hash, parents = [v.decode() for v in line.split(b"^")][:2]
        commits.append(hash)
        tree[hash]["parents"] = parents.split(" ")
        tree[hash]["row"] = row
    return commits, tree

