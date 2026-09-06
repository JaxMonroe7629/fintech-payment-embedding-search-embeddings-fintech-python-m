from fintech_service import PaymentEvent, audit_notification, decide_payment, search_documents


def main() -> None:
    event = PaymentEvent("pay_1001", "acct_42", 12500.0, "USD", "GB")
    decision = decide_payment(event)
    print(audit_notification(event, decision))
    print("Embedding search requires INFRAI_API_KEY:", "fintech embeddings search")
    if __import__("os").environ.get("INFRAI_API_KEY"):
        print(search_documents("chargeback policy", ["Chargeback review policy", "Payroll schedule"]))


if __name__ == "__main__":
    main()
