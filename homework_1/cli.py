import sys
import click

from text_utils import number_lines, count_elements, get_last_lines


@click.group("text_tool")
def text_tool():
    """A command-line tool for text processing."""
    pass


@text_tool.command("number")
@click.argument("input_file", required=False)
def number_lines_command(input_file: str):
    """Add line numbers to the input file or standard input."""
    for num, text in number_lines(input_file):
        formatted_num = f"{num}".rjust(6, " ")
        sys.stdout.write(f"{formatted_num}\t{text}")


@text_tool.command("count")
@click.argument("input_files", nargs=-1)
def count_elements_command(input_files: tuple[str]):
    """Count lines, words, and bytes in the input file(s) or standard input."""
    summary = {"lines": 0, "words": 0, "bytes": 0}

    if input_files:
        for file in input_files:
            result = count_elements(file)
            summary["lines"] += result["lines"]
            summary["words"] += result["words"]
            summary["bytes"] += result["bytes"]

            lines = str(result["lines"]).rjust(7, " ")
            words = str(result["words"]).rjust(7, " ")
            bytes = str(result["bytes"]).rjust(7, " ")
            sys.stdout.write(f" {lines} {words} {bytes} {file}\n")

        if len(input_files) > 1:
            total_lines = str(summary["lines"]).rjust(7, " ")
            total_words = str(summary["words"]).rjust(7, " ")
            total_bytes = str(summary["bytes"]).rjust(7, " ")
            sys.stdout.write(f" {total_lines} {total_words} {total_bytes} total\n")
    else:
        result = count_elements()
        lines = str(result["lines"]).rjust(7, " ")
        words = str(result["words"]).rjust(7, " ")
        bytes = str(result["bytes"]).rjust(7, " ")
        sys.stdout.write(f" {lines} {words} {bytes}\n")


@click.command("end")
@click.argument("input_files", nargs=-1)
def show_end_lines_command(input_files: tuple[str]):
    """Display the last lines of the input file(s) or standard input."""
    if input_files:
        for idx, file in enumerate(input_files):
            try:
                if len(input_files) > 1:
                    sys.stdout.write(f"==> {file} <==\n")

                last_lines = get_last_lines(file)
                if last_lines:
                    sys.stdout.write("\n".join(last_lines))

                if idx < len(input_files) - 1:
                    sys.stdout.write("\n\n")
            except FileNotFoundError:
                sys.stderr.write(f"Ошибка: Файл '{file}' не найден.\n")
            except Exception as e:
                sys.stderr.write(f"Ошибка: {e}\n")
    else:
        try:
            last_lines = get_last_lines()
            if last_lines:
                sys.stdout.write("".join(last_lines))
        except Exception as e:
            sys.stderr.write(f"Ошибка: {e}\n")


text_tool.add_command(number_lines_command)
text_tool.add_command(count_elements_command)
text_tool.add_command(show_end_lines_command)


if __name__ == "__main__":
    text_tool()
