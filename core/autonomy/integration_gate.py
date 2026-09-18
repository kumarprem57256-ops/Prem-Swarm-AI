"""Final gate: integrate only after verification passes."""
from __future__ import annotations
import hashlib, shutil, time
from pathlib import Path

class IntegrationGate:
    def __init__(self, root: str | Path, backup_dir: str | Path):
        self.root=Path(root).resolve()
        self.backup_dir=Path(backup_dir)
        self.backup_dir.mkdir(parents=True,exist_ok=True)

    def backup(self, rel: str) -> Path | None:
        target=self.root/rel
        if not target.exists(): return None
        stamp=time.strftime("%Y%m%d-%H%M%S")
        out=self.backup_dir/f"{stamp}__{rel.replace('/','__')}"
        out.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(target,out)
        return out

    def snapshot_hash(self, rel: str) -> str | None:
        p=self.root/rel
        if not p.exists(): return None
        return hashlib.sha256(p.read_bytes()).hexdigest()

    def allowed(self, rel: str) -> bool:
        p=Path(rel)
        blocked={".git",".env","credentials.json"}
        return not any(part in blocked for part in p.parts) and not p.name.endswith((".key",".pem"))
