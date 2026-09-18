"""Structured autonomous architecture planning."""
from __future__ import annotations
import json
from dataclasses import dataclass, field, asdict
from typing import List

@dataclass
class FileChange:
    action: str
    path: str
    content: str = ""
    reason: str = ""

@dataclass
class BuildPlan:
    pillar_id: str
    summary: str
    changes: List[FileChange] = field(default_factory=list)
    tests: List[str] = field(default_factory=list)
    integration_points: List[str] = field(default_factory=list)

class AutonomousArchitect:
    SYSTEM = """You are PREM Swarm's principal software architect.
Return ONLY valid JSON. Never propose secrets, destructive shell commands,
or unrelated rewrites. Prefer minimal modular changes and preserve working code."""
    def __init__(self, model):
        self.model=model

    def create_plan(self, spec: dict, workspace: dict, context: str) -> BuildPlan:
        prompt=f"""PILLAR SPEC:
{json.dumps(spec, indent=2)}

WORKSPACE SUMMARY:
{json.dumps({k:v for k,v in workspace.items() if k != "hashes"}, indent=2)}

RELEVANT SOURCE:
{context}

Return JSON with:
pillar_id, summary, changes[], tests[], integration_points[].
Each change must have action=create|modify, path, content, reason.
Do not modify tests unless needed. Do not touch .git or secrets.
"""
        r=self.model.generate(self.SYSTEM,prompt)
        if r.error or not r.text.strip():
            return BuildPlan(spec["pillar_id"], spec["objective"],
                             tests=["python -m compileall -q ."])
        text=r.text.strip()
        if text.startswith("```"):
            text=text.split("\n",1)[1].rsplit("```",1)[0].strip()
        try:
            obj=json.loads(text)
            changes=[]
            for c in obj.get("changes",[]):
                if c.get("action") in ("create","modify") and c.get("path"):
                    changes.append(FileChange(**{
                        "action":c["action"], "path":c["path"],
                        "content":c.get("content",""), "reason":c.get("reason","")
                    }))
            return BuildPlan(
                pillar_id=obj.get("pillar_id",spec["pillar_id"]),
                summary=obj.get("summary",spec["objective"]),
                changes=changes,
                tests=obj.get("tests",["python -m compileall -q ."]),
                integration_points=obj.get("integration_points",[]),
            )
        except Exception:
            return BuildPlan(spec["pillar_id"], spec["objective"],
                             tests=["python -m compileall -q ."])
