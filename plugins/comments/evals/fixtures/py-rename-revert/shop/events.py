from shop import handlers


def balance_change(event):
    """Change to the customer's balance in cents for one event, by its type."""
    return getattr(handlers, "on_" + event["type"])(event)
