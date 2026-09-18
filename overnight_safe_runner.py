#!/usr/bin/env python3

import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE_DIR = ROOT / ".swarm_builder" / "overnight"
STATE_FILE = STATE_DIR / "state.json"
LOG_FILE = STATE_DIR / "overnight.log"

TESTS = [
    ".phase2_incoming/extracted/tests/test_phase2_autonomy.py",
    "tests/test_phase2_v2_adapter.py",
    "tests/test_phase2_e2e_adapter.py",
    "tests/test_phase2_method_contracts.py",
]

def now():
    return datetime.now(timezone.utc).isoformat()

def log(message):
    line = f"[{now()}] {message}"
    print(line, flush=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

def save_state(state):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(state, indent=2),
        encoding="utf-8"
    )

def run_tests():
    cmd = [
        "python", "-m", "pytest", "-q",
        *TESTS,
    ]

    env = dict(__import__("os").environ)
    env["PYTHONPATH"] = f"{ROOT}:{ROOT / '.phase2_incoming/extracted'}"

    result = subprocess.run(
        cmd,
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )

    return result.returncode, result.stdout, result.stderr

def main():
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    state = {
        "runner": "PREM_SWARM_SAFE_OVERNIGHT",
        "started_at": now(),
        "mode": "SAFE_VERIFICATION_ONLY",
        "cycles": 0,
        "successful_cycles": 0,
        "failed_cycles": 0,
        "status": "RUNNING",
        "code_generation": False,
        "generated_code_execution": False,
        "autonomous_filesystem_mutation": False,
        "external_llm": False,
    }

    save_state(state)

    log("=" * 70)
    log("PREM SWARM AI — SAFE OVERNIGHT RUNNER")
    log("=" * 70)
    log("Mode: SAFE_VERIFICATION_ONLY")
    log("Code generation: DISABLED")
    log("Generated code execution: DISABLED")
    log("Autonomous filesystem mutation: DISABLED")
    log("External LLM: DISABLED")
    log("")

    # Run indefinitely until interrupted.
    while True:
        state["cycles"] += 1
        cycle = state["cycles"]

        log(f"--- CYCLE {cycle} START ---")

        rc, stdout, stderr = run_tests()

        if stdout.strip():
            for line in stdout.strip().splitlines():
                log(line)

        if stderr.strip():
            for line in stderr.strip().splitlines():
                log("STDERR: " + line)

        if rc == 0:
            state["successful_cycles"] += 1
            log(f"✅ CYCLE {cycle} PASS")
        else:
            state["failed_cycles"] += 1
            state["status"] = "STOPPED_ON_FAILURE"
            state["stopped_at"] = now()
            save_state(state)

            log(f"🛑 CYCLE {cycle} FAILED")
            log("Runner stopped. No autonomous modification was performed.")
            break

        state["last_pass_at"] = now()
        save_state(state)

        log(f"--- CYCLE {cycle} COMPLETE ---")
        log("Waiting 5 minutes before next verification cycle...")
        time.sleep(300)

if __name__ == "__main__":
    main()
