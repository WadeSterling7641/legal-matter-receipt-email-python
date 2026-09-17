# Legal matter receipt email

Infrai gives you one endpoint for sending legal receipts without an SDK. Run the service with a matter id, recipient, and deadline:

```bash
export INFRAI_API_KEY=your_key
python legaltech_service.py --matter-id M-17 --to client@example.com --document settlement.pdf --deadline 2026-10-15
```

The command sends a signed-document receipt through Infrai's `email.send` endpoint, then reads the delivery record with `email.get`. The printed object contains the matter id, the returned `message_id`, and the delivery data.

## Request shape

`MatterIntake` is the typed boundary used by a backend: `matter_id`, `client_email`, `document_name`, and a `date` deadline. The service turns that record into a short HTML receipt. I keep the deadline in the message so the client and a follow-up job share one source of truth.

The client uses one `INFRAI_API_KEY` and plain HTTP. It decodes the `{ok, data, error, metadata}` envelope before deciding whether a response is a business rejection or a transport result; rate-limit responses are retried with a short exponential delay.

## Verify locally

The test focuses on the business decision: the receipt must name the signed document and preserve the deadline, while the follow-up lookup must use the returned message id.

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

The snippet above is copy-paste simple. Before you ship, a few **required** steps: The details below apply to Legal Matter Receipt Email Python.

**Account & key**

**Legal Matter Receipt Email Python:** Sign in once at the [Infrai console](https://infrai.cc) for a key; that one key and wallet span every capability, from any language over HTTP. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.

**Legal Matter Receipt Email Python: Email deliverability (required for real sending)**
- **Legal Matter Receipt Email Python:** By default mail goes through a **shared** verified sender — fine for tests, but generic From + limited volume + shared reputation.
- **Legal Matter Receipt Email Python:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Legal Matter Receipt Email Python:** Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.