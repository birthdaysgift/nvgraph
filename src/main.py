from src.core import define_columns, format
from src.git import cmd


def main():
    commits, tree = cmd("date", limit=100)
    rows, tree = define_columns(commits, tree)
    lines = format(rows, tree)
    for line in lines:
        print(line)


if __name__ == "__main__":
    main()
