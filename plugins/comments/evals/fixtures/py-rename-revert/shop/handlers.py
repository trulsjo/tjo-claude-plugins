# ref = refund
def on_ref(event):
    """Amount in cents to credit back to the customer for a refund event."""
    return event["amount_cents"]


def on_sale(event):
    """Amount in cents to charge the customer for a sale event."""
    return -event["amount_cents"]
