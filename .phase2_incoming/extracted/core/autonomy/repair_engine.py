"""Minimal model-driven repair proposal generator."""
from __future__ import annotations
import json

class RepairEngine:
    SYSTEM="""You are a senior Python repair engineer.
Return ONLY JSON: {"path":"...", "content":"...", "reason":"..."}.
Make the smallest repair necessary. Never remove unrelated functionality."""
    def __init__(self, model):
        self.model=model

    def propose(self, failure: str, changed_files: list[str], context: str) -> dict | None:
        prompt=f"""FAILURE:
{failure[-12000:]}

CHANGED FILES:
{json.dumps(changed_files, indent=2)}

SOURCE CONTEXT:
{context[:30000]}
"""
        r=self.model.generate(self.SYSTEM,prompt)
        if r.error or not r.text.strip(): return None
        text=r.text.strip()
        if text.startswith("```"):
            text=text.split("\n",1)[1].rsplit("```",1)[0].strip()
        try:
            obj=json.loads(text)
            if not obj.get("path") or not isinstance(obj.get("content"),str): return None
            return obj
        except Exception:
            return None
