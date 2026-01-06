from script import cmd, parse, format


def main():
    test_topo_order()
    test_date_order()
    test_author_date_order()


def test_topo_order():
    print("    - Testing topo order...", end=" ")
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
            " |  |  * cd4fb90e",
            " |  |  |  * aa90f5b5",
            " |  |  |  * 73be2336",
            " |  |  |  * c23d0115",
            " |  |  |  * 63a4ddc9",
            " |  |  |  * 4bb05125",
            " |  |  |  * a313d25e",
            " |  |  |  * 24d8b291",
            " |  |  |  * f704b53d",
            " |  |  |  * 3c5a2e10",
            " |  |  |  * 721957e3",
            " |  |  |  * f1a2b0fe",
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
            " |  * 1fb02d4f",
            " |  * 72b5fb17",
            " |  * e8793bc0",
            " |  * f5e34fb1",
            " |  * 6ab11ec7",
            " |  * f459374a",
            " |  * 320c224c",
            " |  * 5e64c392",
            " |  * 82ea7d06",
            " |  |  |  |  * ddbb8951",
            " |  |  |  |  * e2ba5753",
        ],
    ):
        assert actual == expected, (actual, expected)
    print("OK")


def test_date_order():
    print("    - Testing date order...", end=" ")
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
            " |  |  |  * aa90f5b5",
            " |  |  |  * 73be2336",
            " |  |  |  * c23d0115",
            " |  |  |  * 63a4ddc9",
            " |  |  |  * 4bb05125",
            " |  |  |  * a313d25e",
            " |  |  |  * 24d8b291",
            " |  |  |  * f704b53d",
            " |  |  |  * 3c5a2e10",
            " |  |  |  * 721957e3",
            " |  |  |  * f1a2b0fe",
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
            " |  |  |  |  * ddbb8951",
            " |  |  * 2b67b414",
            " |  |  |  |  * e2ba5753",
            " |  |  |  |  * d920b747",
            " |  |  |  |  * 81316e22",
            " |  |  |  |  * 088e38fe",
            " |  |  |  |  * 37489416",
            " |  |  |  |  * 1f208e4f",
            " |  |  |  |  * 323559ec",
            " |  |  * 1fb02d4f",
            " |  |  * 72b5fb17",
            " |  |  * e8793bc0",
        ],
    ):
        assert actual == expected, (actual, expected)
    print("OK")


def test_author_date_order():
    print("    - Testing author-date order...", end=" ")
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
            " |  |  |  * aa90f5b5",
            " |  |  |  * 73be2336",
            " |  |  |  * c23d0115",
            " |  |  |  * 63a4ddc9",
            " |  |  |  * 4bb05125",
            " |  |  |  * a313d25e",
            " |  |  |  * 24d8b291",
            " |  |  |  * f704b53d",
            " |  |  |  |  * ddbb8951",
            " |  |  |  |  * e2ba5753",
            " |  |  |  |  * d920b747",
            " |  |  |  |  * 81316e22",
            " |  |  |  |  * 088e38fe",
            " |  |  |  |  * 37489416",
            " |  |  |  |  * 1f208e4f",
            " |  |  |  |  * 323559ec",
            " |  |  |  |  |  * 890506e0",
            " |  |  |  |  |  |  * 8c4c0d76",
            " |  |  |  |  |  |  * e734d8c5",
            " |  |  |  |  |  |  * 66949257",
            " |  |  |  |  |  |  * 3a4998b2",
            " |  |  |  |  |  |  * 25284536",
            " |  |  |  |  |  |  * b43c609f",
            " |  |  |  |  |  |  * 6c567755",
            " |  |  |  |  |  |  * c692d020",
            " |  |  |  |  |  |  * 6c99e165",
            " |  |  |  |  |  |  |  * dc873994",
            " |  |  |  |  |  |  |  |  * 115f220e",
            " |  |  |  * 3c5a2e10",
            " |  |  |  * 721957e3",
            " |  |  |  * f1a2b0fe",
            " * 725eb54b",
            " |  * 70d99918",
            " * f6d72a43",
            " |  * 3a4c1120",
        ],
    ):
        assert actual == expected, (actual, expected)
    print("OK")


if __name__ == "__main__":
    main()
