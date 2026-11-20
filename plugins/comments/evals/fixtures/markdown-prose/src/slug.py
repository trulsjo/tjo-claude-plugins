def slugify(title):
    """Lower-case URL slug for a title: ASCII letters and digits joined by single hyphens.

    Returns an empty string when the title has no letters or digits.
    """
    words = "".join(c.lower() if c.isascii() and c.isalnum() else " " for c in title).split()
    return "-".join(words)
