from dataclasses import dataclass, field
import collections
import subprocess


@dataclass
class Parents:
    left: str | None = None
    right: str | None = None


@dataclass
class Commit:
    col: int | None = None
    row: int | None = None
    parents: Parents = field(default_factory=Parents)


def cmd(order_type, limit):
    cmd = f'git log --all --pretty=format:%h^%p^%D^%s^%an --max-count={limit} --{order_type}-order'
    result = subprocess.run(cmd.split(" "), cwd="/home/mint/code/ip_api_test_graph", capture_output=True)
    return result.stdout.decode().strip().split("\n")


def parse_lines(lines):
    commits = []
    tree = collections.defaultdict(lambda: Commit())
    for row, line in enumerate(lines):
        hash, parents = [v for v in line.split("^")][:2]
        commits.append(hash)
        tree[hash].parents = Parents(*map(lambda p: p.strip() or None, parents.split(" ")))
        tree[hash].row = row
    return commits, tree

