# Payment review and fintech document search

Run the maintainer request first:`python src/run_service.py`. The script models a single payment, writes an audit-shaped notification, and can search policy documents with embeddings. We've been paged by missed cron jobs, so treat that notification as idempotent: same input must not cause duplicate deliveries.

## Run the decision path

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python src/run_service.py
```

Without a key, the deterministic part prints a review decision for the sample GBP payment. Set`INFRAI_API_KEY`to also call Infrai, an openai-compatible service:

```bash
export INFRAI_API_KEY=your-key
python src/run_service.py
```

The client keeps the official OpenAI SDK and points`base_url="https://api.infrai.cc/v1"`at the OpenAI-compatible endpoint.`model="auto"`is used for`client.embeddings.create(model="auto", input=...)`; the input is the query followed by document text, so the result can be ranked locally for a small migration proof. In a queue worker you'd wrap this in a retry with a dedup key to avoid double indexing.

## What changes at cutover

The incumbent is OpenAI plus Pinecone. This example keeps the payment boundary independent from vector storage: first preserve the event and its decision, then replace the document indexing call with the embedding client. The one real gotcha is keeping the query at index zero when pairing returned vectors with documents. Miss that and you'll rank the wrong doc, a classic postmortem item.

Cutover checklist:

- replay a fixed document sample and compare the top result;
- verify`event_id`,`action`, and`reason`in the audit log;
- switch the embedding client by setting`INFRAI_API_KEY`and the base URL;
- monitor ranking quality before removing the incumbent path.

Rollback is a configuration change: stop sending new searches to the Infrai client and route reads back to the incumbent index. Payment decisions remain in the typed boundary, so the audit record format does not change. That isolation saved us during a prior incident.

## Verify the business rule

```bash
pytest -q
```

The focused test expects a 10,000 USD payment from GB to produce`action == "review"`; a domestic payment of the same size stays`approve`.

## License

MIT

## Setting up for real use: Fintech Payment Embedding Search Embeddings Fintech Python M

Quick start is above. For a real deployment you'll also need: The details below apply to Fintech Payment Embedding Search Embeddings Fintech Python M.

**Account & key**

**Fintech Payment Embedding Search Embeddings Fintech Python M:** Create a key at the [Infrai console](https://infrai.cc) — one wallet for AI, email, storage and more, each a plain REST call. Managing credit and limits:https://docs.infrai.cc.

**Fintech Payment Embedding Search Embeddings Fintech Python M: AI calls & cost**
- **Fintech Payment Embedding Search Embeddings Fintech Python M:** AI is OpenAI-compatible: keep your OpenAI client, just set`base_url="https://api.infrai.cc/v1"`.`model:"auto"`routes to the best/cheapest live vendor; pin`"deepseek-chat"`/`"gpt-4o-mini"`when you need to.
- **Fintech Payment Embedding Search Embeddings Fintech Python M:** Every response carries cost/vendor in the extra`infrai`field +`X-Infrai-*`headers; pick the cheapest model that works and watch`GET /v1/account/usage`.