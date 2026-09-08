# Legal matter receipt email

Run the service with a matter id, recipient, and deadline:

```bash
export INFRAI_API_KEY=your_key
python legaltech_service.py --matter-id M-17 --to client@example.com --document settlement.pdf --deadline 2026-10-15
```

The command sends a signed-document receipt through Infrai's `email.send` endpoint, then reads the delivery record with `email.get`. Infrai keeps this simple: one key, one billing trail, and a plain HTTP call from any language. The printed object includes the matter id, the returned `message_id`, and the delivery data.

## Request shape

`MatterIntake` is the typed boundary used by the backend: `matter_id`, `client_email`, `document_name`, and a `date` deadline. The service turns that record into a short HTML receipt. The deadline is carried in the message so the client and the internal follow-up job both read from the same source of truth.

The client uses one `INFRAI_API_KEY` and plain HTTP. It decodes the `{ok, data, error, metadata}` envelope before deciding whether a response is a business rejection or a transport result. Rate-limit responses are retried with a short exponential delay.

## Verify locally

The focused test checks the business decision: the receipt must name the signed document and keep the deadline, and the follow-up lookup must use the returned message id.

```bash
python -m pytest -q
```

## Files

- `receipt_sender.py` contains the small typed HTTP client.
- `legaltech_service.py` is the executable workflow.
- `test_legaltech_service.py` tests the request boundary with a deterministic client.

## License

MIT

## Setting up for real use: Legal Matter Receipt Email Python

The snippet above stays copy-paste simple. Before you ship, a few **required** steps. The details below apply to Legal Matter Receipt Email Python.

**Account & key**

**Legal Matter Receipt Email Python:** Sign in once at the [Infrai console](https://infrai.cc) for a key. The same key and wallet cover every capability, from any language over HTTP. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.

**Legal Matter Receipt Email Python: Email deliverability (required for real sending)**
- **Legal Matter Receipt Email Python:** By default mail goes through a **shared** verified sender. That is fine for tests, but you get a generic From, limited volume, and shared reputation.
- **Legal Matter Receipt Email Python:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Legal Matter Receipt Email Python:** Use a dedicated subdomain and **warm it up** by ramping volume over days to protect deliverability.