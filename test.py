from script import cmd, parse, format


def main():
    test_topo_order()
    test_date_order()
    test_author_date_order()


def test_topo_order():
    print("    - Testing topo order...")
    for actual, expected in zip(
        format(*parse(cmd("topo"))),
        [
            " * 69466d6e",
            " |  * a75fec18",
            " * f9aa9635",
            " |  * 2b01f7e5",
            " * 194893b2",
            " |  |  * f7360a37",
            " * 848af9ac",
            " |  * 13618c4f",
            " * dbdea912",
            " |  * ea952a23",
            " |  * 737b913f",
            " * ff3f77b8",
            " |  * c9b97671",
            " |  * 64e4a085",
            " * 725eb54b",
            " |  * 70d99918",
            " * f6d72a43",
            " |  * 3a4c1120",
            " |  * a9871737",
            " * 548b6520",
            " |  |  * e131eaa2",
            " * 0ed1e93f",
            " |  * ddebd7e4",
            " * 8965d3cc",
            " |  * db234819",
            " |  * 575ca088",
            " |  * 2b67b414",
            " |  * 1fb02d4f",
            " |  * 72b5fb17",
            " |  * e8793bc0",
            " |  * f5e34fb1",
            " |  * 6ab11ec7",
            " |  * f459374a",
            " |  * 320c224c",
            " |  * 5e64c392",
            " |  * 82ea7d06",
            " * d36e4fc6",
            " |  * 9a70a712",
            " |  * 191fbcb7",
            " * 9032e8e1",
            " |  |  * a5c55a3a",
            " |  |  * d1e1a29f",
            " |  |  |  * cd4fb90e",
            " |  |  |  |  * 8c4c0d76",
            " |  |  |  |  * e734d8c5",
            " |  |  |  |  * 66949257",
            " |  |  |  |  * 3a4998b2",
            " |  |  |  |  * 25284536",
            " |  |  |  |  * b43c609f",
            " |  |  |  |  * 6c567755",
        ],
    ):
        assert actual == expected, (actual, expected)
    print("OK")


def test_date_order():
    print("    - Testing date order...")
    for actual, expected in zip(
        format(*parse(cmd("date"))),
        [
            " * 69466d6e",
            " |  * a75fec18",
            " * f9aa9635",
            " * 194893b2",
            " |  * cd4fb90e",
            " |  |  * f7360a37",
            " |  |  |  * 2b01f7e5",
            " * 848af9ac",
            " |  |  * 13618c4f",
            " * dbdea912",
            " |  |  * ea952a23",
            " |  |  * 737b913f",
            " * ff3f77b8",
            " |  |  * c9b97671",
            " |  |  * 64e4a085",
            " * 725eb54b",
            " |  |  * 70d99918",
            " * f6d72a43",
            " |  |  * 3a4c1120",
            " |  |  * a9871737",
            " * 548b6520",
            " |  |  |  * e131eaa2",
            " * 0ed1e93f",
            " |  |  * ddebd7e4",
            " * 8965d3cc",
            " |  |  * db234819",
            " |  |  * 575ca088",
            " |  |  * 2b67b414",
            " |  |  * 1fb02d4f",
            " |  |  * 72b5fb17",
            " |  |  * e8793bc0",
            " |  |  * f5e34fb1",
            " |  |  * 6ab11ec7",
            " |  |  * f459374a",
            " |  |  * 320c224c",
            " |  |  * 5e64c392",
            " |  |  * 82ea7d06",
            " * d36e4fc6",
            " * 9032e8e1",
            " |  |  * a5c55a3a",
            " |  |  * d1e1a29f",
            " |  |  |  * 9a70a712",
            " |  |  |  * 191fbcb7",
            " |  |  |  |  * 8c4c0d76",
            " |  |  |  |  * e734d8c5",
            " |  |  |  |  * 66949257",
            " |  |  |  |  * 3a4998b2",
            " |  |  |  |  * 25284536",
            " |  |  |  |  * b43c609f",
            " |  |  |  |  * 6c567755",
        ],
    ):
        assert actual == expected, (actual, expected)
    print("OK")


def test_author_date_order():
    print("    - Testing author-date order...")
    for actual, expected in zip(
        format(*parse(cmd("author-date"))),
        [
            " * 69466d6e",
            " |  * a75fec18",
            " * f9aa9635",
            " * 194893b2",
            " |  * f7360a37",
            " |  |  * cd4fb90e",
            " |  |  |  * 2b01f7e5",
            " * 848af9ac",
            " |  * 13618c4f",
            " * dbdea912",
            " |  * ea952a23",
            " |  * 737b913f",
            " * ff3f77b8",
            " |  * c9b97671",
            " |  * 64e4a085",
            " * 725eb54b",
            " |  * 70d99918",
            " * f6d72a43",
            " |  * 3a4c1120",
            " |  * a9871737",
            " * 548b6520",
            " |  |  |  * e131eaa2",
            " * 0ed1e93f",
            " |  * ddebd7e4",
            " * 8965d3cc",
            " |  * db234819",
            " |  * 575ca088",
            " |  * 2b67b414",
            " |  |  |  |  * 8c4c0d76",
            " |  * 1fb02d4f",
            " |  |  |  |  * e734d8c5",
            " |  * 72b5fb17",
            " |  |  |  |  * 66949257",
            " |  * e8793bc0",
            " |  |  |  |  * 3a4998b2",
            " |  * f5e34fb1",
            " |  |  |  |  * 25284536",
            " |  * 6ab11ec7",
            " |  |  |  |  * b43c609f",
            " |  * f459374a",
            " |  |  |  |  * 6c567755",
            " |  * 320c224c",
            " |  |  |  |  * c692d020",
            " |  * 5e64c392",
            " |  |  |  |  * 6c99e165",
            " |  * 82ea7d06",
            " * d36e4fc6",
            " * 9032e8e1",
            " |  * a5c55a3a",
            " |  * d1e1a29f",
        ],
    ):
        assert actual == expected, (actual, expected)
    print("OK")


if __name__ == "__main__":
    main()
