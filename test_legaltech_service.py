from datetime import date

from legaltech_service import MatterIntake, send_matter_receipt
from receipt_sender import EmailResult


class StubClient:
    def __init__(self):
        self.sent = None

    def send(self, **kwargs):
        self.sent = kwargs
        return EmailResult("msg-42")

    def get(self, message_id):
        return {"message_id": message_id, "status": "delivered"}


def test_receipt_contains_deadline_and_signed_document():
    client = StubClient()
    matter = MatterIntake("M-17", "client@example.com", "settlement.pdf", date(2026, 10, 15))
    result = send_matter_receipt(matter, client)
    assert client.sent["to"] == "client@example.com"
    assert "settlement.pdf" in client.sent["html"]
    assert "2026-10-15" in client.sent["html"]
    assert result["delivery"]["status"] == "delivered"

