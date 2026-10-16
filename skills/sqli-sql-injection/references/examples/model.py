"""Synthetic SQLite example; connections are supplied by the offline test."""

def names(connection, term, sort, restrict_sort=False):
    columns = {"name": "name", "created": "created"}
    if restrict_sort:
        if sort not in columns:
            raise ValueError("unsupported sort")
        sort = columns[sort]
    sql = "SELECT name FROM catalog WHERE name LIKE ? ORDER BY " + sort
    return [row[0] for row in connection.execute(sql, ("%" + term + "%",))]
