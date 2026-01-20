from time import perf_counter

from src.core import define_columns, format
from src.git import cmd


def main():
    start = perf_counter()
    commits, tree = cmd("date", limit=100)
    rows, tree = define_columns(commits, tree)
    lines = format(rows, tree)
    for line in lines:
        print(line)
    stop = perf_counter()
    print(f"Commits: {len(commits)}")
    print(f"Elapsed: {stop - start}")


if __name__ == "__main__":
    main()
