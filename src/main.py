from src.core import parse_tree, format
from src.git import cmd


def main():
    commits_data = cmd("topo", limit=100)
    commits, tree = parse_tree(commits_data)
    lines = format(commits, tree)
    for line in lines:
        print(line)


if __name__ == "__main__":
    main()
