import os
import json
import urllib.request
import subprocess
import sqlite3

class CodeArchitectAgent:
    def __init__(self, db_name="swarm_execution_memory.db"):
        self.db_name = db_name
        self.groq_api_key = os.getenv("GROQ_API_KEY", "").strip()

    def generate_local_fallback(self, module_name):
        print("💡 [LOCAL FALLBACK] Generating Python tool locally...")
        return f'''import sqlite3

def run_task():
    conn = sqlite3.connect("swarm_execution_memory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("📊 [SELF-BUILT LOCAL TOOL: {module_name}]")
    print("Found Tables:", tables)
    conn.close()

if __name__ == "__main__":
    run_task()
'''

    def generate_tool_code(self, task_objective, module_name):
        print(f"\n🧬 [CODE ARCHITECT] Synthesizing module for: '{task_objective}'...")
        if not self.groq_api_key:
            print("⚠️ GROQ_API_KEY Missing. Using Local Template.")
            return self.generate_local_fallback(module_name)

        prompt = (
            f"Write a standalone, error-free Python script for: '{task_objective}'. "
            "Output ONLY valid Python code inside markdown ```python ... ```. No text."
        )

        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            payload = json.dumps({
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": "You are an expert Python Auto-Coder Agent."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2,
                "max_tokens": 1000
            }).encode('utf-8')

            req = urllib.request.Request(
                url, data=payload,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.groq_api_key}',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                },
                method='POST'
            )

            with urllib.request.urlopen(req, timeout=10) as resp:
                res_data = json.loads(resp.read().decode('utf-8'))
                raw_code = res_data['choices'][0]['message']['content']
                
                if "```python" in raw_code:
                    code = raw_code.split("```python")[1].split("```")[0].strip()
                elif "```" in raw_code:
                    code = raw_code.split("```")[1].split("```")[0].strip()
                else:
                    code = raw_code.strip()
                return code
        except Exception as e:
            print(f"⚠️ Groq API Error ({e}). Switching to Local Fallback Architecture.")
            return self.generate_local_fallback(module_name)

    def build_and_integrate(self, module_name, task_objective):
        code = self.generate_tool_code(task_objective, module_name)
        filename = f"auto_{module_name}.py"
        filepath = os.path.join(os.path.expanduser("~/Prem_Swarm_AI"), filename)

        with open(filepath, "w") as f:
            f.write(code)

        print(f"📝 Script Written: {filename}")

        try:
            res = subprocess.run(["python3", "-m", "py_compile", filepath], capture_output=True, text=True)
            if res.returncode == 0:
                print(f"✅ [SELF-BUILDING SUCCESS] {filename} passed syntax compilation!")
                self.log_tool(filename, task_objective, "SUCCESS")
                return True
            else:
                print(f"⚠️ Syntax Error in generated tool: {res.stderr}")
                self.log_tool(filename, task_objective, "FAILED_SYNTAX")
                return False
        except Exception as e:
            print(f"❌ Execution Test Error: {e}")
            return False

    def log_tool(self, filename, objective, status):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO task_history (task_description, category, status, result, timestamp)
            VALUES (?, ?, ?, ?, datetime('now', 'localtime'))
        ''', (f"Self-Built Tool: {filename}", "AUTO_CODE_EVOLUTION", status, f"Objective: {objective}"))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    architect = CodeArchitectAgent()
    architect.build_and_integrate("data_cleaner", "A script that reads sqlite database swarm_execution_memory.db and prints summary statistics.")
