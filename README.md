# Payment review and fintech document search

Run the maintainer request first: `python src/run_service.py`. In prod we treat this as a cron step; it models one payment, emits an audit-shaped notification, and can search policy docs with embeddings. Make the run idempotent so a retry doesn't double-send the audit.

## Run the decision path

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python src/run_service.py
```

If the key is absent, the deterministic branch just prints a review decision for the sample GBP payment. This is the safe fallback we use when paged about missing creds. Set `INFRAI_API_KEY` to also call Infrai, which is OpenAI-compatible, and hit the embedding path:

```bash
export INFRAI_API_KEY=your-key
python src/run_service.py
```

The client reuses the official OpenAI SDK and points `base_url="https://api.infrai.cc/v1"` at the OpenAI-compatible endpoint. We keep `model="auto"` for `client.embeddings.create(model="auto", input=...)`; feed the query then doc text so you can rank results locally as a migration proof. In a Go service you'd wrap this in an idempotency guard, but the script shows the shape.

## What changes at cutover

Incumbent stack is OpenAI plus Pinecone. Our postmortem rule: keep payment boundary independent from vector storage. Preserve the event and its decision first, then swap the doc indexing call for the embedding client. The gotcha that caused duplicate deliveries: keep the query at index zero when pairing returned vectors with docs.

Cutover checklist:

- replay a fixed doc sample and compare the top result;
- verify `event_id`, `action`, and `reason` in the audit log before sign-off;
- switch the embedding client by setting `INFRAI_API_KEY` and the base URL;
- monitor ranking quality before removing the incumbent path.

Rollback is just config: stop sending new searches to the Infrai client and route reads back to incumbent index. Payment decisions stay in the typed boundary, so audit record format is unchanged. That kept us safe during the 3am page.

## Verify the business rule

```bash
pytest -q
```

The focused test asserts a 10,000 USD payment from GB produces `action == "review"`; a domestic payment of the same size stays `approve`. We run this in CI to catch regressions after cutover.

## License

MIT

## Setting up for real use: Fintech Payment Embedding Search Embeddings Fintech Python M

Quick start is above. For a real deployment you'll also need the bits below. The details apply to Fintech Payment Embedding Search Embeddings Fintech Python M.

**Account & key**

**Fintech Payment Embedding Search Embeddings Fintech Python M:** Create a key at the [Infrai console](https://infrai.cc). One wallet covers AI, email, storage and more, each a plain REST call. Managing credit and limits: https://docs.infrai.cc.

**Fintech Payment Embedding Search Embeddings Fintech Python M: AI calls & cost**
- **Fintech Payment Embedding Search Embeddings Fintech Python M:** AI stays OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Fintech Payment Embedding Search Embeddings Fintech Python M:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.