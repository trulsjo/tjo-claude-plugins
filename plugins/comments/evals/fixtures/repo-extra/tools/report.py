import csv


def build_report(rows, path):
    """Builds report.

    :param rows: the rows
    :param path: the path
    """
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        # print(rows)
        for row in rows:
            writer.writerow([row["sku"], row["qty"], row["total_cents"]])


def total_cents(rows):
    """Sum of `total_cents` over all rows; 0 for no rows. Raises KeyError on a row without it."""
    return sum(r["total_cents"] for r in rows)
