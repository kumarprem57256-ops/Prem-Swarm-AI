"""Provider-neutral LLM adapter for PREM Swarm Phase 2.

No credentials are stored in source. The default provider uses an
OpenAI-compatible HTTP endpoint configured through environment variables.
It can therefore point at an existing compatible gateway without coupling
the autonomous developer to one vendor.
"""
from __future__ import annotations
import json, os, urllib.request, urllib.error
from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class ModelResponse:
    text: str = ""
    provider: str = "none"
    model: str = ""
    error: Optional[str] = None

class ModelAdapter:
    def __init__(self, timeout: int = 90):
        self.timeout = timeout
        self.provider = os.getenv("PREM_LLM_PROVIDER", "none").lower()
        self.endpoint = os.getenv("PREM_LLM_ENDPOINT", "").strip()
        self.model = os.getenv("PREM_LLM_MODEL", "").strip()
        self.api_key = os.getenv("PREM_LLM_API_KEY", "").strip()

    def configured(self) -> bool:
        return bool(self.endpoint and self.model and self.api_key)

    def generate(self, system: str, prompt: str, *,
                 temperature: float = 0.1,
                 max_tokens: int = 12000) -> ModelResponse:
        if not self.configured():
            return ModelResponse(provider="none", model=self.model,
                                 error="PREM_LLM_ENDPOINT/MODEL/API_KEY not configured")
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint, data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                raw = json.loads(r.read().decode("utf-8"))
            text = raw.get("choices", [{}])[0].get("message", {}).get("content", "")
            if not isinstance(text, str):
                text = str(text)
            return ModelResponse(text=text, provider=self.provider,
                                 model=self.model)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
                json.JSONDecodeError, KeyError, IndexError) as exc:
            return ModelResponse(provider=self.provider, model=self.model,
                                 error=f"{type(exc).__name__}: {exc}")
