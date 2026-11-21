def export_csv(rows):
    # TODO(#142): quote fields that contain a newline
    return "\n".join(",".join(map(str, r)) for r in rows)
