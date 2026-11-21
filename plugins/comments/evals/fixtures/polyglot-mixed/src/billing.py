# Copyright (c) 2026 Example Shop AS. Licensed under the MIT License.

from decimal import Decimal


def invoice_total(invoices):
    """Sum of the open invoices' amounts, in NOK.

    Paid invoices are skipped. Returns Decimal("0") when no invoice is open.
    Raises ValueError if an invoice has a negative amount.
    """
    # loop over the invoices and add up the open ones
    total = Decimal("0")
    for inv in invoices:
        if inv.amount < 0:
            raise ValueError("negative amount")
        if not inv.paid:
            total += inv.amount
    # print("total", total)
    return total


def get_customer(customer_id):
    """Gets the customer.

    :param customer_id: the customer id
    :returns: the customer
    """
    return _CUSTOMERS[customer_id]  # type: ignore[index]


_CUSTOMERS = {}
