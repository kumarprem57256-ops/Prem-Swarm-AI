#!/usr/bin/env python3

"""
PREM SWARM AI
Autonomous Pillar Builder V2

Pipeline:
Specification
 -> Workspace Analysis
 -> Architecture Plan
 -> Implementation
 -> Validation
 -> Review
 -> Repair
 -> Regression Check
 -> Integration
 -> State/Memory

IMPORTANT:
- Never blindly overwrite existing files.
- Creates backups before modifying existing files.
- Uses an adapter hook for the actual AI model.
- Starts in SAFE/PLAN mode unless explicitly approved.
"""

from __future__ import annotations

import ast
import json
import os
import shutil
import subprocess
import sys
import time
import hashlib
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional


# ============================================================
# CONFIGURATION
# ============================================================

ROOT = Path.cwd().resolve()

STATE_DIR = ROOT / ".swarm_builder"
STATE_FILE = STATE_DIR / "pillar_state.json"
PLAN_DIR = STATE_DIR / "plans"
BACKUP_DIR = STATE_DIR / "backups"
LOG_FILE = STATE_DIR / "builder.log"

MAX_REPAIR_ATTEMPTS = 3
MAX_FILE_SIZE = 500_000


# ============================================================
# UTILITIES
# ============================================================

def ensure_dirs() -> None:
    STATE_DIR.mkdir(exist_ok=True)
    PLAN_DIR.mkdir(exist_ok=True)
    BACKUP_DIR.mkdir(exist_ok=True)


def log(message: str) -> None:
    ensure_dirs()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_state() -> Dict[str, Any]:
    ensure_dirs()

    if not STATE_FILE.exists():
        return {
            "version": 2,
            "pillars": {},
            "history": [],
        }

    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        log("WARNING: State file unreadable. Starting fresh state.")
        return {
            "version": 2,
            "pillars": {},
            "history": [],
        }


def save_state(state: Dict[str, Any]) -> None:
    ensure_dirs()

    temp = STATE_FILE.with_suffix(".tmp")
    temp.write_text(
        json.dumps(state, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    temp.replace(STATE_FILE)


# ============================================================
# DATA MODELS
# ============================================================

@dataclass
class PillarSpec:
    pillar_id: str
    name: str
    objective: str
    requirements: List[str]
    constraints: List[str]
    acceptance_criteria: List[str]
    priority: str = "normal"


@dataclass
class FileChange:
    path: str
    action: str
    reason: str
    content: Optional[str] = None


@dataclass
class BuildPlan:
    pillar_id: str
    summary: str
    changes: List[FileChange]
    tests: List[str]


# ============================================================
# PROJECT ANALYZER
# ============================================================

class WorkspaceAnalyzer:

    IGNORED_DIRS = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".swarm_builder",
        "node_modules",
    }

    def scan(self) -> Dict[str, Any]:
        log("🔍 Scanning Swarm workspace...")

        python_files: List[str] = []
        directories: List[str] = []

        for root, dirs, files in os.walk(ROOT):
            dirs[:] = [
                d for d in dirs
                if d not in self.IGNORED_DIRS
            ]

            relative_root = Path(root).relative_to(ROOT)

            if str(relative_root) != ".":
                directories.append(str(relative_root))

            for filename in files:
                if filename.endswith(".py"):
                    path = Path(root) / filename

                    try:
                        if path.stat().st_size <= MAX_FILE_SIZE:
                            python_files.append(
                                str(path.relative_to(ROOT))
                            )
                    except OSError:
                        pass

        return {
            "root": str(ROOT),
            "python_files": sorted(python_files),
            "directories": sorted(directories),
            "python_file_count": len(python_files),
        }


# ============================================================
# MODEL ADAPTER
# ============================================================

class ModelAdapter:
    """
    Central AI adapter.

    Replace only this layer when connecting:
    - Groq
    - OpenAI-compatible endpoint
    - Gemini
    - local model
    - future PREM/NEXUS model

    The rest of the builder should remain model-agnostic.
    """

    def generate(self, system: str, prompt: str) -> str:
        # Safe local fallback.
        # This deliberately DOES NOT pretend to be a real LLM.
        log("⚠️ No external/local model adapter configured.")
        return ""


# ============================================================
# ARCHITECT
# ============================================================

class AutonomousArchitect:

    def __init__(self, model: ModelAdapter):
        self.model = model

    def create_plan(
        self,
        spec: PillarSpec,
        workspace: Dict[str, Any],
    ) -> BuildPlan:

        log(f"🧠 Architect analyzing pillar: {spec.pillar_id}")

        prompt = f"""
PILLAR:
{json.dumps(asdict(spec), indent=2)}

WORKSPACE:
{json.dumps(workspace, indent=2)}

Design a production-grade implementation plan.

Requirements:
1. Preserve existing architecture where possible.
2. Do not unnecessarily rewrite working modules.
3. Identify new modules only when required.
4. Define integration points.
5. Define verification tests.
6. Prefer small modular changes.
"""

        # Until a real model is connected, create a conservative plan.
        model_output = self.model.generate(
            "You are the principal architect of a modular autonomous software system.",
            prompt,
        )

        if model_output.strip():
            # Future: structured JSON parsing.
            pass

        return BuildPlan(
            pillar_id=spec.pillar_id,
            summary=spec.objective,
            changes=[],
            tests=[
                "python -m compileall -q .",
            ],
        )


# ============================================================
# SAFE FILE MANAGER
# ============================================================

class SafeFileManager:

    def backup(self, relative_path: str) -> Optional[Path]:
        target = ROOT / relative_path

        if not target.exists():
            return None

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        safe_name = relative_path.replace("/", "__")
        backup = BACKUP_DIR / f"{timestamp}__{safe_name}"

        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, backup)

        log(f"💾 Backup created: {backup}")
        return backup

    def write(
        self,
        relative_path: str,
        content: str,
        allow_existing: bool = False,
    ) -> bool:

        target = ROOT / relative_path

        if target.exists() and not allow_existing:
            log(
                f"🛡️ BLOCKED overwrite: {relative_path}"
            )
            return False

        if len(content.encode("utf-8")) > MAX_FILE_SIZE:
            log(
                f"🛡️ BLOCKED oversized generated file: {relative_path}"
            )
            return False

        target.parent.mkdir(parents=True, exist_ok=True)

        if target.exists():
            self.backup(relative_path)

        temp = target.with_suffix(target.suffix + ".tmp")

        temp.write_text(
            content,
            encoding="utf-8",
        )

        temp.replace(target)

        log(f"💾 File committed: {relative_path}")
        return True


# ============================================================
# CODE VALIDATOR
# ============================================================

class Validator:

    def syntax_check(self, path: Path) -> bool:
        try:
            source = path.read_text(encoding="utf-8")
            ast.parse(source, filename=str(path))
            return True
        except Exception as exc:
            log(f"❌ Syntax failure: {path}: {exc}")
            return False

    def compile_project(self) -> bool:
        log("🧪 Running Python compilation check...")

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "compileall",
                "-q",
                str(ROOT),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            log("✅ Project compilation PASS")
            return True

        log("❌ Project compilation FAIL")

        if result.stderr:
            log(result.stderr[-4000:])

        return False

    def pytest(self) -> bool:
        pytest = shutil.which("pytest")

        if not pytest:
            log("ℹ️ pytest not installed; skipping pytest stage.")
            return True

        log("🧪 Running pytest...")

        result = subprocess.run(
            [pytest, "-q"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            log("✅ pytest PASS")
            return True

        log("❌ pytest FAIL")

        output = (result.stdout + "\n" + result.stderr)[-5000:]
        log(output)

        return False


# ============================================================
# REVIEWER
# ============================================================

class Reviewer:

    def review(
        self,
        spec: PillarSpec,
        workspace: Dict[str, Any],
        plan: BuildPlan,
    ) -> Dict[str, Any]:

        issues: List[str] = []

        if not spec.name.strip():
            issues.append("Pillar name is empty.")

        if not spec.objective.strip():
            issues.append("Pillar objective is empty.")

        if not spec.acceptance_criteria:
            issues.append(
                "No acceptance criteria supplied."
            )

        return {
            "approved": not issues,
            "issues": issues,
        }


# ============================================================
# PILLAR BUILDER
# ============================================================

class AutonomousPillarBuilder:

    def __init__(self):
        ensure_dirs()

        self.state = load_state()
        self.analyzer = WorkspaceAnalyzer()
        self.model = ModelAdapter()
        self.architect = AutonomousArchitect(self.model)
        self.files = SafeFileManager()
        self.validator = Validator()
        self.reviewer = Reviewer()

    def register_pillar(self, spec: PillarSpec) -> None:

        self.state["pillars"][spec.pillar_id] = {
            "spec": asdict(spec),
            "status": "registered",
            "attempts": 0,
        }

        save_state(self.state)

        log(
            f"📌 Registered pillar: "
            f"{spec.pillar_id} — {spec.name}"
        )

    def build(self, spec: PillarSpec) -> bool:

        log("")
        log("=" * 70)
        log(
            f"🚀 BUILDING PILLAR "
            f"{spec.pillar_id}: {spec.name}"
        )
        log("=" * 70)

        self.register_pillar(spec)

        workspace = self.analyzer.scan()

        self.state["pillars"][spec.pillar_id]["status"] = (
            "analyzing"
        )
        save_state(self.state)

        plan = self.architect.create_plan(
            spec,
            workspace,
        )

        plan_path = (
            PLAN_DIR /
            f"{spec.pillar_id.replace('/', '_')}.json"
        )

        plan_path.write_text(
            json.dumps(
                asdict(plan),
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        log(f"🧠 Plan saved: {plan_path}")

        review = self.reviewer.review(
            spec,
            workspace,
            plan,
        )

        if not review["approved"]:
            log("❌ Architecture review rejected.")

            for issue in review["issues"]:
                log(f"   • {issue}")

            self.state["pillars"][spec.pillar_id][
                "status"
            ] = "blocked"

            save_state(self.state)
            return False

        self.state["pillars"][spec.pillar_id]["status"] = (
            "planned"
        )
        save_state(self.state)

        # ----------------------------------------------------
        # IMPORTANT:
        # Actual AI-generated file changes are intentionally
        # not auto-applied until the model adapter is connected.
        # ----------------------------------------------------

        if not plan.changes:
            log(
                "ℹ️ No executable file changes generated yet."
            )
            log(
                "ℹ️ Connect ModelAdapter.generate() "
                "before autonomous implementation."
            )

            self.state["pillars"][spec.pillar_id][
                "status"
            ] = "planned_only"

            save_state(self.state)
            return True

        # ----------------------------------------------------
        # Apply changes safely
        # ----------------------------------------------------

        self.state["pillars"][spec.pillar_id]["status"] = (
            "implementing"
        )
        save_state(self.state)

        for change in plan.changes:

            if change.action == "create":
                if not self.files.write(
                    change.path,
                    change.content or "",
                    allow_existing=False,
                ):
                    return False

            elif change.action == "modify":
                if not self.files.write(
                    change.path,
                    change.content or "",
                    allow_existing=True,
                ):
                    return False

            else:
                log(
                    f"⚠️ Unknown change action: "
                    f"{change.action}"
                )
                return False

        # ----------------------------------------------------
        # Validation + repair loop
        # ----------------------------------------------------

        for attempt in range(
            1,
            MAX_REPAIR_ATTEMPTS + 1,
        ):

            self.state["pillars"][spec.pillar_id][
                "attempts"
            ] = attempt

            save_state(self.state)

            log(
                f"🔬 Verification attempt "
                f"{attempt}/{MAX_REPAIR_ATTEMPTS}"
            )

            compile_ok = self.validator.compile_project()

            if compile_ok:
                test_ok = self.validator.pytest()

                if test_ok:
                    log(
                        "🏆 PILLAR VERIFICATION PASS"
                    )

                    self.state["pillars"][
                        spec.pillar_id
                    ]["status"] = "completed"

                    save_state(self.state)
                    return True

            if attempt < MAX_REPAIR_ATTEMPTS:
                log(
                    "🔧 Verification failed. "
                    "Repair cycle required."
                )

                # Future model-driven repair hook.
                repair_result = self.model.generate(
                    "You are a senior debugging and repair engineer.",
                    "Analyze the latest project validation "
                    "failure and produce a minimal safe repair.",
                )

                if not repair_result:
                    log(
                        "⚠️ No repair model connected."
                    )
                    break

        self.state["pillars"][spec.pillar_id][
            "status"
        ] = "failed"

        save_state(self.state)

        log(
            f"❌ Pillar failed verification: "
            f"{spec.pillar_id}"
        )

        return False

    def status(self) -> None:

        print("")
        print("=" * 70)
        print("PREM SWARM AUTONOMOUS PILLAR BUILDER")
        print("=" * 70)

        pillars = self.state.get("pillars", {})

        if not pillars:
            print("No pillars registered.")
            return

        for pillar_id, data in pillars.items():

            print(
                f"{pillar_id:12} "
                f"{data.get('status', 'unknown'):15} "
                f"attempts={data.get('attempts', 0)}"
            )


# ============================================================
# EXAMPLE SPECIFICATION LOADER
# ============================================================

def load_specs() -> List[PillarSpec]:

    spec_file = ROOT / "pillar_specs.json"

    if not spec_file.exists():

        example = [
            {
                "pillar_id": "pillar-01",
                "name": "Example Pillar",
                "objective": "Replace this with the real pillar objective.",
                "requirements": [
                    "Define exact capabilities.",
                ],
                "constraints": [
                    "Preserve existing working architecture.",
                ],
                "acceptance_criteria": [
                    "All relevant tests pass.",
                    "No existing core functionality regresses.",
                ],
                "priority": "high",
            }
        ]

        spec_file.write_text(
            json.dumps(
                example,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        log(
            "📄 Created pillar_specs.json template."
        )

        return []

    raw = json.loads(
        spec_file.read_text(encoding="utf-8")
    )

    specs: List[PillarSpec] = []

    for item in raw:

        specs.append(
            PillarSpec(
                pillar_id=item["pillar_id"],
                name=item["name"],
                objective=item["objective"],
                requirements=item.get(
                    "requirements",
                    [],
                ),
                constraints=item.get(
                    "constraints",
                    [],
                ),
                acceptance_criteria=item.get(
                    "acceptance_criteria",
                    [],
                ),
                priority=item.get(
                    "priority",
                    "normal",
                ),
            )
        )

    return specs


# ============================================================
# CLI
# ============================================================

def main() -> None:

    ensure_dirs()

    builder = AutonomousPillarBuilder()

    if len(sys.argv) < 2:

        print("")
        print("PREM SWARM AUTONOMOUS PILLAR BUILDER V2")
        print("")
        print("Usage:")
        print("  python autonomous_pillar_builder.py status")
        print("  python autonomous_pillar_builder.py scan")
        print("  python autonomous_pillar_builder.py plan")
        print("  python autonomous_pillar_builder.py build")
        print("")
        return

    command = sys.argv[1].lower()

    if command == "status":

        builder.status()

    elif command == "scan":

        workspace = builder.analyzer.scan()

        print(
            json.dumps(
                workspace,
                indent=2,
                ensure_ascii=False,
            )
        )

    elif command == "plan":

        specs = load_specs()

        if not specs:
            print(
                "Add your real pillars to pillar_specs.json first."
            )
            return

        for spec in specs:

            builder.register_pillar(spec)

            workspace = builder.analyzer.scan()

            plan = builder.architect.create_plan(
                spec,
                workspace,
            )

            print("")
            print(
                f"PLAN: {spec.pillar_id} — {spec.name}"
            )
            print(
                json.dumps(
                    asdict(plan),
                    indent=2,
                    ensure_ascii=False,
                )
            )

    elif command == "build":

        specs = load_specs()

        if not specs:
            print(
                "No pillar specifications found."
            )
            return

        log(
            f"🚀 Autonomous build queue: "
            f"{len(specs)} pillars"
        )

        for index, spec in enumerate(
            specs,
            start=1,
        ):

            log(
                f"📦 Queue "
                f"{index}/{len(specs)}: "
                f"{spec.pillar_id}"
            )

            success = builder.build(spec)

            if not success:
                log(
                    "🛑 Queue paused because "
                    "verification failed."
                )
                break

        builder.status()

    else:

        print(
            f"Unknown command: {command}"
        )


if __name__ == "__main__":
    main()
