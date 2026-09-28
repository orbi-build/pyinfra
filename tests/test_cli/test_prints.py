from pyinfra_cli.prints import _display_width, print_rows


def _column_start(line: str, marker: str) -> int:
    """Display column at which ``marker`` starts in ``line``."""
    return _display_width(line[: line.index(marker)])


def test_display_width_counts_wide_and_fullwidth_as_two():
    # Narrow / halfwidth characters take one cell each
    assert _display_width("ascii") == 5
    # East Asian wide characters take two cells each
    assert _display_width("中文") == 4
    # Fullwidth Latin letters take two cells each
    assert _display_width("ＡＢＣ") == 6


def test_display_width_ignores_ansi_codes():
    assert _display_width("\033[1mhello\033[0m") == 5


def test_print_rows_pads_cjk_columns_by_display_width():
    output: list[str] = []

    cjk_name = "随便输出一些中文试试"

    print_rows(
        [
            (output.append, ["Operation", "Status"]),
            (output.append, ["short", "ok"]),
            (output.append, [cjk_name, "ok"]),
        ]
    )

    # The header, the ASCII-only row and the CJK row all reserve the same
    # display width for the first column, so the second column starts at the
    # same display column in every row.
    starts = [
        _column_start(output[0], "Status"),
        _column_start(output[1], "ok"),
        _column_start(output[2], "ok"),
    ]

    assert starts[0] == starts[1] == starts[2]


def test_print_rows_pads_fullwidth_columns_by_display_width():
    output: list[str] = []

    print_rows(
        [
            (output.append, ["Name", "State"]),
            (output.append, ["ok", "yes"]),
            (output.append, ["ＡＢＣ", "yes"]),
        ]
    )

    starts = [
        _column_start(output[0], "State"),
        _column_start(output[1], "yes"),
        _column_start(output[2], "yes"),
    ]

    assert starts[0] == starts[1] == starts[2]
