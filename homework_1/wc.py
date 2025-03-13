import sys
from collections import defaultdict

__all__ = ["wc"]


def wc(filename: str | None = None) -> dict[str, int]:
    statistics = defaultdict(int)

    with open(filename, "r") if filename else sys.stdin as file:
        lines = file.readlines()
        statistics["lines"] = len(lines)
        statistics["words"] = sum(len(line.split()) for line in lines)
        statistics["bytes"] = sum(len(line.encode("utf-8")) for line in lines)

    return dict(statistics)
