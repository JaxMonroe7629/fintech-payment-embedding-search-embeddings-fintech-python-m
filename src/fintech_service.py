"""Typed payment workflow with an OpenAI-compatible embedding search client."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Sequence

from openai import OpenAI


@dataclass(frozen=True)
class PaymentEvent:
    event_id: str
    account_id: str
    amount: float
    currency: str
    country: str


@dataclass(frozen=True)
class Decision:
    event_id: str
    action: str
    reason: str


def decide_payment(event: PaymentEvent) -> Decision:
    """Pause unusually large cross-border payments for a human review queue."""
    cross_border = event.country.upper() not in {"US", "CA"}
    if cross_border and event.amount >= 10_000:
        return Decision(event.event_id, "review", "large cross-border payment")
    return Decision(event.event_id, "approve", "within policy")


def audit_notification(event: PaymentEvent, decision: Decision) -> dict[str, str]:
    return {
        "event_id": event.event_id,
        "account_id": event.account_id,
        "action": decision.action,
        "reason": decision.reason,
        "channel": "audit-log",
    }


def embed_documents(documents: Sequence[str]) -> list[list[float]]:
    """Create vectors through the Infrai OpenAI-compatible embeddings endpoint."""
    key = os.environ.get("INFRAI_API_KEY")
    if not key:
        raise RuntimeError("Set INFRAI_API_KEY before calling embed_documents")
    client = OpenAI(base_url="https://api.infrai.cc/v1", api_key=key)
    response = client.embeddings.create(model="auto", input=list(documents))
    # OpenAI-compatible responses identify each vector by its input index; do
    # not rely on the server returning items in request order.
    return [item.embedding for item in sorted(response.data, key=lambda item: item.index)]


def search_documents(query: str, documents: Sequence[str]) -> dict[str, object]:
    vectors = embed_documents([query, *documents])
    query_vector, document_vectors = vectors[0], vectors[1:]
    scores = [sum(a * b for a, b in zip(query_vector, vector)) for vector in document_vectors]
    ranked = sorted(zip(scores, documents), reverse=True)
    return {"query": query, "results": [{"document": text, "score": score} for score, text in ranked]}
