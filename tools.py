# tools.py

import random

from datetime import datetime
from datetime import timedelta


def get_order_status(order_id: str) -> str:

    print("RUNNING ORDER STATUS TOOL")

    if order_id == "UNKNOWN":

        return (
            "No order ID was found in the message. "
            "Please provide your order ID."
        )

    statuses = [

        (
            "Order is being processed and will ship "
            "within 1-2 business days."
        ),

        (
            "Order has shipped. Expected delivery: "
            + (
                datetime.now() + timedelta(days=3)
            ).strftime("%B %d, %Y")
            + "."
        ),

        (
            "Order was delivered on "
            + (
                datetime.now() - timedelta(days=1)
            ).strftime("%B %d, %Y")
            + "."
        ),

        "Order is out for delivery today."
    ]

    status = random.choice(statuses)

    return f"Order {order_id}: {status}"


def process_refund(order_id: str) -> str:

    print("RUNNING REFUND TOOL")

    if order_id == "UNKNOWN":

        return (
            "No order ID was found. "
            "Please provide your order ID to process the refund."
        )

    return (
        f"Refund for order {order_id} has been initiated. "
        f"The amount will be credited back within 5-7 business days."
    )


def get_billing_info() -> str:

    print("RUNNING BILLING TOOL")

    last_invoice_date = (
        datetime.now() - timedelta(days=10)
    ).strftime("%B %d, %Y")

    next_billing_date = (
        datetime.now() + timedelta(days=20)
    ).strftime("%B %d, %Y")

    return (
        f"Last invoice: $49.99 charged on {last_invoice_date}. "
        f"Payment method: Visa ending in 4242. "
        f"Next billing date: {next_billing_date}."
    )