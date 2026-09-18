import os, json, time, subprocess, pathlib, hashlib, shutil, requests, sys

ROOT = pathlib.Path.cwd()
STATE_DIR = ROOT / ".swarm_builder" / "developer"
STATE_DIR.mkdir(parents=True, exist_ok=True)
STATE_FILE = STATE_DIR / "state.json"
LOG_FILE = STATE_DIR / "developer.log"
BACKUP_DIR = STATE_DIR / "backups"
BACKUP_DIR.mkdir(exist_ok=True)

MODEL = os.getenv("PREM_LLM_MODEL", "openai/gpt-oss-120b")
ENDPOINT = os.getenv(
    "PREM_LLM_ENDPOINT",
    "https://api.groq.com/openai/v1/chat/completions"
)
API_KEY = os.getenv("GROQ_API_KEY")

KNOWN = {
    1: "Fractal Planner",
    2: "Entropic Chaos Mitigator",
    3: "Context Compaction",
    4: "Neuro-Symbolic Synaptic Memory",
}

def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {
        "completed": [1, 2, 3],
        "current": 4,
        "status": "STARTING",
        "history": []
    }

def save_state(s):
    STATE_FILE.write_text(json.dumps(s, indent=2), encoding="utf-8")

def snapshot():
    stamp = time.strftime("%Y%m%d-%H%M%S")
    dst = BACKUP_DIR / stamp
    dst.mkdir()
    for p in ROOT.iterdir():
        if p.name in {".git", ".swarm_builder", ".env"}:
            continue
        if p.is_dir():
            shutil.copytree(p, dst / p.name, ignore=shutil.ignore_patterns(
                "__pycache__", ".pytest_cache", "*.pyc"
            ))
        else:
            shutil.copy2(p, dst / p.name)
    return dst

def pytest():
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=ROOT, text=True, capture_output=True
    )
    return r.returncode == 0, (r.stdout + "\n" + r.stderr)[-12000:]

def source_text():
    candidates = [
        ROOT / "09_ORIGINAL_ROADMAP_INBOX.md",
        ROOT / "08_RECOVERY_RULES.md",
        ROOT / "07_ROADMAP.md",
        ROOT / "05_IMPLEMENTATION_STATUS.md",
        ROOT / "01_PILLARS_01-05.md",
        ROOT / "02_PILLARS_06-15.md",
        ROOT / "03_IDEAS_CATALOG.md",
        ROOT / "04_ARCHITECTURE.md",
    ]
    chunks = []
    for p in candidates:
        if p.exists():
            chunks.append(f"\n===== {p.name} =====\n")
            chunks.append(p.read_text(errors="ignore")[:30000])
    return "".join(chunks)

def ask(prompt):
    if not API_KEY:
        raise RuntimeError("GROQ_API_KEY not detected")

    r = requests.post(
        ENDPOINT,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are PREM Developer AI. "
                        "You MUST obey source-grounding. "
                        "Never invent missing pillar definitions. "
                        "Return strict JSON only."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            "temperature": 0,
            "max_tokens": 8000
        },
        timeout=120
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"].get("content", "")

def main():
    log("========================================")
    log("PREM DEVELOPER AI — AUTONOMOUS MODE")
    log(f"MODEL: {MODEL}")
    log("========================================")

    if not API_KEY:
        log("STOP: GROQ_API_KEY missing")
        return 2

    state = load_state()
    state["status"] = "RUNNING"
    save_state(state)

    ok, out = pytest()
    if not ok:
        log("STOP: baseline pytest is RED")
        log(out)
        state["status"] = "BASELINE_FAILED"
        save_state(state)
        return 1

    log("BASELINE TESTS GREEN")

    for pillar in range(4, 16):
        if pillar in state["completed"]:
            continue

        name = KNOWN.get(pillar, "UNRECOVERED")

        if name == "UNRECOVERED":
            log(
                f"STOP: Pillar #{pillar} definition is not "
                "verified from the recovered master sources."
            )
            state["current"] = pillar
            state["status"] = "WAITING_FOR_SOURCE_DEFINITION"
            save_state(state)
            return 0

        log(f"START PILLAR #{pillar}: {name}")

        backup = snapshot()
        log(f"BACKUP: {backup}")

        prompt = f"""
PILLAR NUMBER: {pillar}
PILLAR NAME: {name}

MASTER SOURCES:
{source_text()}

TASK:
Determine whether the source material actually defines this pillar.
If it does not, STOP.

If it does:
1. inspect the existing repository architecture,
2. propose the smallest safe implementation,
3. preserve V1/V2 compatibility,
4. identify files to change,
5. define tests,
6. return JSON with:
{{
  "source_verified": true/false,
  "implementation_required": true/false,
  "reason": "...",
  "plan": ["..."],
  "files": ["..."],
  "tests": ["..."]
}}

Do NOT write code yet.
"""
        try:
            raw = ask(prompt)
            log("ARCHITECT RESPONSE RECEIVED")
            log(raw[:6000])
        except Exception as e:
            log(f"STOP: architect request failed: {e}")
            state["status"] = "LLM_ERROR"
            save_state(state)
            return 1

        try:
            data = json.loads(raw)
        except Exception:
            log("STOP: LLM did not return valid JSON")
            state["status"] = "INVALID_ARCHITECT_RESPONSE"
            save_state(state)
            return 1

        if not data.get("source_verified", False):
            log(f"STOP: source definition unavailable for #{pillar}")
            state["status"] = "WAITING_FOR_SOURCE_DEFINITION"
            save_state(state)
            return 0

        log(
            f"Pillar #{pillar} is source-verified. "
            "Implementation gate intentionally stops before code mutation "
            "in this bootstrap controller."
        )
        state["current"] = pillar
        state["status"] = "IMPLEMENTATION_GATE"
        save_state(state)
        return 0

    state["status"] = "ALL_RECOVERED_PILLARS_COMPLETE"
    save_state(state)
    log("ALL RECOVERED PILLARS COMPLETE")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
