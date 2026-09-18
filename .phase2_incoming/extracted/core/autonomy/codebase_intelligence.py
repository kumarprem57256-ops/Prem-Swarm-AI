"""Read-only project intelligence for autonomous planning."""
from __future__ import annotations
import ast, hashlib
from pathlib import Path
from typing import Any, Dict, List, Set

IGNORED = {".git", ".venv", "venv", "__pycache__", ".pytest_cache",
           ".mypy_cache", ".swarm_builder", "node_modules"}
MAX_BYTES = 300_000

class CodebaseIntelligence:
    def __init__(self, root: str | Path):
        self.root = Path(root).resolve()

    def scan(self) -> Dict[str, Any]:
        modules=[]; imports={}; symbols={}; hashes={}
        for p in self.root.rglob("*.py"):
            if any(part in IGNORED for part in p.parts): continue
            try:
                if p.stat().st_size > MAX_BYTES: continue
                src=p.read_text(encoding="utf-8")
                rel=str(p.relative_to(self.root))
                tree=ast.parse(src, filename=rel)
                modules.append(rel)
                imports[rel]=sorted({
                    n.module or "" for n in tree.body
                    if isinstance(n, ast.ImportFrom)
                } | {
                    n.name for n in tree.body if isinstance(n, ast.Import)
                })
                symbols[rel]=sorted(
                    [n.name for n in tree.body
                     if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
                )
                hashes[rel]=hashlib.sha256(src.encode()).hexdigest()
            except (OSError, UnicodeError, SyntaxError):
                continue
        return {
            "root": str(self.root),
            "python_files": sorted(modules),
            "imports": imports,
            "symbols": symbols,
            "hashes": hashes,
            "python_file_count": len(modules),
        }

    def relevant_context(self, spec: Dict[str, Any], limit: int = 80_000) -> str:
        data=self.scan()
        keywords=set()
        for field in ("name","objective"):
            keywords.update(str(spec.get(field,"")).lower().split())
        keywords.update(str(x).lower() for x in spec.get("requirements",[]))
        ranked=[]
        for path in data["python_files"]:
            hay=(path+" "+" ".join(data["symbols"].get(path,[]))).lower()
            score=sum(1 for k in keywords if len(k)>2 and k in hay)
            ranked.append((score,path))
        ranked.sort(reverse=True)
        selected=ranked[:40]
        chunks=[]
        for _, path in selected:
            p=self.root/path
            try:
                src=p.read_text(encoding="utf-8")
            except Exception: continue
            chunks.append(f"\n### FILE: {path}\n{src[:6000]}")
            if sum(map(len,chunks)) >= limit: break
        return "".join(chunks)[:limit]
