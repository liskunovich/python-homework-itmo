import sys


def nl(filename: str | None = None):
    if filename:
        with open(filename, "r") as file:
            for line_number, line in enumerate(file, start=1):
                yield line_number, line
    else:
        for line_number, line in enumerate(sys.stdin, start=1):
            yield line_number, line
