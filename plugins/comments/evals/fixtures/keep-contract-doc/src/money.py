def split_amount(total_cents, parts):
    """Split an amount into near-equal parts that sum to the total.

    The first ``total_cents % parts`` parts get one extra cent.
    Raises ValueError if parts is less than 1.
    """
    if parts < 1:
        raise ValueError("parts must be at least 1")
    base, extra = divmod(total_cents, parts)
    return [base + 1 if i < extra else base for i in range(parts)]
