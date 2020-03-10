from beautifultable import BeautifulTable



def get_table(cols, rows, max_width=120) -> BeautifulTable:
    """Returns a table ready for printing to stdout.
    
    :param cols: Table columns.
    :param rows: Table rows.
    :param max_width: Maximum table width in characters.

    """
    # Set table data.
    t = BeautifulTable(max_width=max_width)
    t.column_headers = cols
    for row in rows:
        t.append_row(row)

    # Set default style.
    t.set_style(BeautifulTable.STYLE_NONE)
    t.top_border_char = "-"
    t.header_separator_char = '-'
    t.bottom_border_char = "-"

    return t    