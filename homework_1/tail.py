import sys


def tail(file_path=None, num_lines=17):
    try:
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
        else:
            lines = sys.stdin.readlines()

        return lines[-num_lines:]
    except FileNotFoundError:
        sys.stderr.write(f"Файл '{file_path}' не найден.\n")
        return []
    except Exception as e:
        sys.stderr.write(f"Ошибка: {e}\n")
        return []
