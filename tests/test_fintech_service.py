from fintech_service import PaymentEvent, decide_payment


def test_large_cross_border_payment_enters_review() -> None:
    event = PaymentEvent("p1", "acct", 10_000, "USD", "GB")
    decision = decide_payment(event)
    assert decision.action == "review"
    assert decision.reason == "large cross-border payment"


def test_domestic_payment_is_approved() -> None:
    event = PaymentEvent("p2", "acct", 20_000, "USD", "US")
    assert decide_payment(event).action == "approve"
