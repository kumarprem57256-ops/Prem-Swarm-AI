"""Verification gates for generated changes."""
from __future__ import annotations
import subprocess, sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

@dataclass
class VerificationResult:
    passed: bool
    stage: str
    output: str = ""
    command: List[str] = field(default_factory=list)

class VerificationEngine:
    def __init__(self, root: str | Path):
        self.root=Path(root).resolve()

    def run(self, command: List[str], stage: str) -> VerificationResult:
        try:
            p=subprocess.run(command,cwd=self.root,text=True,capture_output=True,timeout=180)
            out=(p.stdout+"\n"+p.stderr)[-12000:]
            return VerificationResult(p.returncode==0,stage,out,command)
        except subprocess.TimeoutExpired as e:
            return VerificationResult(False,stage,f"timeout: {e}",command)

    def all(self) -> List[VerificationResult]:
        results=[self.run([sys.executable,"-m","compileall","-q","."],"compile")]
        pytest=self.root/"pytest.ini"
        if pytest.exists() or list(self.root.glob("test*.py")) or (self.root/"tests").exists():
            results.append(self.run([sys.executable,"-m","pytest","-q"],"pytest"))
        return results
