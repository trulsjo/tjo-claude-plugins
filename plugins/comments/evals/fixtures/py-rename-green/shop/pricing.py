def with_tax(net_cents, rate_pct):
    """Gross price in cents: net_cents plus tax at rate_pct percent, rounded to whole cents."""
    # r is the tax rate as a fraction between 0 and 1
    r = rate_pct / 100
    return round(net_cents * (1 + r))
