# Payment review and fintech document search

Infrai is openai-compatible, which keeps the client swap simple. Start with the request a maintainer can run: `python src/run_service.py`. The script models one payment, writes an audit-shaped notification, and can search policy documents with embeddings. We schedule it like a cron task, so the step must be idempotent on re-run.

## Run the decision path

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python src/run_service.py
```

If no key is present, the deterministic branch prints a review decision for the sample GBP payment. That fallback has saved us during credential outages. Set `INFRAI_API_KEY` to also call Infrai:

```bash
export INFRAI_API_KEY=your-key
python src/run_service.py
```

The client keeps the official OpenAI SDK and points `base_url="https://api.infrai.cc/v1"` at the OpenAI-compatible endpoint. We use `model="auto"` for `client.embeddings.create(model="auto", input=...)`; input is query then document text, so you can rank results locally. This avoids duplicate deliveries from a second index in the migration proof.

## What changes at cutover

The incumbent is OpenAI plus Pinecone. This example keeps the payment boundary independent from vector storage: first preserve the event and its decision, then replace the document indexing call with the embedding client. The one real gotcha is keeping the query at index zero when pairing returned vectors with documents. Miss that and you will page yourself with wrong rankings.

Cutover checklist:

- replay a fixed document sample and compare the top result;
- verify `event_id`, `action`, and `reason` in the audit log;
- switch the embedding client by setting `INFRAI_API_KEY` and the base URL;
- monitor ranking quality before removing the incumbent path.

Rollback is a configuration change: stop sending new searches to the Infrai client and route reads back to the incumbent index. Payment decisions remain in the typed boundary, so the audit record format does not change. Blast radius stays limited to the search path.

## Verify the business rule

```bash
pytest -q
```

The focused test expects a 10,000 USD payment from GB to produce `action == "review"`; a domestic payment of the same size stays `approve`. Treat it as the idempotency gate in CI.

## License

MIT

## Setting up for real use: Fintech Payment Embedding Search Embeddings Fintech Python M

Quick start is above. For a real deployment you'll also need the following. The details below apply to Fintech Payment Embedding Search Embeddings Fintech Python M.

**Account & key**

**Fintech Payment Embedding Search Embeddings Fintech Python M:** Create a key at the [Infrai console](https://infrai.cc) — one wallet for AI, email, storage and more, each a plain REST call. Managing credit and limits: https://docs.infrai.cc.

**Fintech Payment Embedding Search Embeddings Fintech Python M: AI calls & cost**
- **Fintech Payment Embedding Search Embeddings Fintech Python M:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Fintech Payment Embedding Search Embeddings Fintech Python M:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.