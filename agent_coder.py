import os
import re
import time
import ast
import requests
from brain.utils import generate_tool_name

class CoderAgent:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def _extract_python(self, text):
        if not text:
            raise ValueError("Empty model response")

        text = text.strip()

        # Remove markdown code fences
        match = re.search(r"```(?:python|py)?\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
        if match:
            text = match.group(1).strip()

        # Remove leading explanatory lines
        lines = text.splitlines()
        while lines:
            first = lines[0].strip()
            if (first.startswith(("import ", "from ", "class ", "def ", "if ")) or first.startswith("#!")) and not first.startswith("1."):
                break
            lines.pop(0)

        text = "\n".join(lines).strip()

        if not text:
            raise ValueError("No Python source detected in output")

        ast.parse(text)
        return text

    def _write_verified(self, filename, code):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"🚀 [Coder-02] Built & Verified Syntax for '{filename}'!")
        return filename

    def build_tool(self, topic, description, failure_context=None):
        filename = generate_tool_name(topic)
        print(f"⚡ [Coder-02] Synthesizing Engine: '{filename}'...")

        repair = ""
        if failure_context:
            repair = f"\nCRITICAL FIX REQUIRED (PREVIOUS FAILURE):\n{failure_context}\nDo NOT block on sys.stdin when running self-tests.\n"

        prompt = f"""
You are a Python code generation engine.

TASK:
{topic}

DESCRIPTION:
{description}

{repair}

STRICT TECHNICAL CONTRACT:
1. Return ONLY executable Python 3 source code. Zero markdown or prose.
2. Use Python standard library modules only.
3. NON-BLOCKING INPUT: If reading stdin, check `if not sys.stdin.isatty():` or wrap stdin calls inside functions so self-tests run non-interactively without waiting forever.
4. ENTRY POINT: The script MUST execute its automated self-tests directly inside `if __name__ == '__main__':` and call `sys.exit(0)` on success.
"""

        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are a strict Python generator. Return complete, valid Python source code only."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.0,
            "max_tokens": 4096
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        for attempt in range(1, 4):
            try:
                response = requests.post(self.url, headers=headers, json=payload, timeout=30)

                if response.status_code == 429:
                    wait = min(30, 3 * attempt)
                    print(f"⚠️ [Coder-02] Rate limited (429). Retrying in {wait}s...")
                    time.sleep(wait)
                    continue

                if response.status_code != 200:
                    print(f"⚠️ HTTP {response.status_code}: {response.text[:150]}")
                    time.sleep(2)
                    continue

                raw = response.json()["choices"][0]["message"]["content"]

                try:
                    code = self._extract_python(raw)
                    return self._write_verified(filename, code)
                except SyntaxError as e:
                    print(f"❌ Syntax Error (Attempt {attempt}): {e}")
                    failure_context = f"Generated Python contains SyntaxError at line {e.lineno}: {e.msg}"
                    time.sleep(1)
                    continue
                except ValueError as e:
                    print(f"❌ Extractor Error (Attempt {attempt}): {e}")
                    failure_context = str(e)
                    time.sleep(1)
                    continue

            except Exception as e:
                print(f"⚠️ [Coder-02] Attempt {attempt} Exception: {e}")
                time.sleep(2 ** attempt)

        return None
