from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from receipt_sender import InfraiEmailClient


@dataclass(frozen=True)
class MatterIntake:
    matter_id: str
    client_email: str
    document_name: str
    deadline: date


def send_matter_receipt(matter: MatterIntake, client: InfraiEmailClient) -> dict[str, Any]:
    """Send the signed-document receipt and return its delivery record."""
    result = client.send(
        to=matter.client_email,
        subject=f"Matter {matter.matter_id}: signed document received",
        html=(
            f"<p>We received <strong>{matter.document_name}</strong> for matter "
            f"<strong>{matter.matter_id}</strong>.</p>"
            f"<p>Next deadline: {matter.deadline.isoformat()}.</p>"
        ),
        request_id=f"matter-{matter.matter_id}-receipt",
    )
    delivery = client.get(result.message_id)
    return {"matter_id": matter.matter_id, "message_id": result.message_id, "delivery": delivery}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Send a legal matter receipt email")
    parser.add_argument("--matter-id", required=True)
    parser.add_argument("--to", required=True)
    parser.add_argument("--document", default="signed engagement letter")
    parser.add_argument("--deadline", required=True, help="ISO date, for example 2026-10-15")
    args = parser.parse_args()
    matter = MatterIntake(args.matter_id, args.to, args.document, date.fromisoformat(args.deadline))
    print(send_matter_receipt(matter, InfraiEmailClient()))

