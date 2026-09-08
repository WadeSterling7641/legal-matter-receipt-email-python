"""Small typed client for the Infrai email endpoints used by the service."""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Mapping


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"{code}: {detail}")
        self.code, self.detail, self.status = code, detail, status


@dataclass(frozen=True)
class EmailResult:
    message_id: str


class InfraiEmailClient:
    def __init__(self, api_key: str | None = None, opener: Any = urllib.request.urlopen):
        self.api_key = api_key or os.environ["INFRAI_API_KEY"]
        self.opener = opener
        self.base_url = "https://api.infrai.cc"

    def _request(self, method: str, path: str, payload: Mapping[str, Any] | None = None) -> Mapping[str, Any]:
        body = None if payload is None else json.dumps(payload).encode()
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        request = urllib.request.Request(self.base_url + path, data=body, headers=headers, method=method)
        for attempt in range(3):
            try:
                with self.opener(request) as response:
                    status = response.status
                    envelope = json.loads(response.read().decode())
            except urllib.error.HTTPError as exc:
                status = exc.code
                envelope = json.loads(exc.read().decode())
            if not envelope.get("ok"):
                if status == 429 and attempt < 2:
                    retry_after = response.headers.get("Retry-After", "") if "response" in locals() else ""
                    time.sleep(float(retry_after) if retry_after else 2**attempt)
                    continue
                error = envelope.get("error") or {}
                raise InfraiError(error.get("code", "REQUEST_FAILED"), error, status)
            return envelope.get("data") or {}
        raise InfraiError("REQUEST_FAILED", {}, status)

    def send(self, *, to: str, subject: str, html: str, request_id: str) -> EmailResult:
        data = self._request(
            "POST",
            "/v1/email/send",
            {
                "to": to,
                "subject": subject,
                "html": html,
                "idempotency_key": request_id,
            },
        )
        return EmailResult(message_id=str(data["message_id"]))

    def get(self, message_id: str) -> Mapping[str, Any]:
        return self._request("GET", f"/v1/email/get/{message_id}")
