from table_generator import build_table, insert_picture


def main():
    data = [
        ["Fruits", "Q-ty", "Price"],
        ["Apple", 10, 15],
        ["Banana", 5, 20],
        ["Orange", 8, 25],
    ]

    table_code = build_table(data)

    figure_code = insert_picture("ratatui.png")

    latex_document = (
        r"""
    \documentclass{article}
    \usepackage{graphicx}  

    \begin{document}

    \section*{ Table}
    """
        + table_code
        + r"""

    \section*{Picture}
    """
        + figure_code
        + r"""

    \end{document}
    """
    )

    tex_filename = "example_output.tex"
    with open(tex_filename, "w", encoding="utf-8") as f:
        f.write(latex_document)

    print(f"LaTeX файл '{tex_filename}' сгенерирован.")


if __name__ == "__main__":
    main()
