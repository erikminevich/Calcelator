from collections.abc import Sequence


def render_pretty_table(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    widths = [len(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    for row in str_rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    def border() -> str:
        return "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def line(cells: Sequence[str]) -> str:
        padded = [f" {cells[i].ljust(widths[i])} " for i in range(len(cells))]
        return "|" + "|".join(padded) + "|"

    output = [border(), line(list(headers)), border()]
    for row in str_rows:
        output.append(line(row))
    output.append(border())
    return "\n".join(output)
