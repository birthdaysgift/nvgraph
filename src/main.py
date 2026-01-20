from time import perf_counter

from src.core import define_columns, format
from src.git import cmd, parse_lines


def main():
    start = perf_counter()
    lines = [
        "A1^A2 B1",
        "C1^C2",
        "B1^A2",
        "A2^A3",
        "C2^C3 D1",
        "D1^D2",
        "D2^C3",
        "C3^C4",
        "C4^A3",
        "A3^"

    ]
    commits, tree = parse_lines(
        # cmd(order_type="date", limit=1000)
        lines
    )
    rows, tree = define_columns(commits, tree)
    lines = format(rows, tree)
    for line in lines:
        print(line)
    stop = perf_counter()
    print(f"Commits: {len(commits)}")
    print(f"Elapsed: {stop - start}")


if __name__ == "__main__":
    main()
