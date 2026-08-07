import subprocess, os, re

class CodeExecutorAgent:
    def __init__(self, agent_id="Agent_04_Executor"):
        self.agent_id = agent_id

    def extract_pure_code(self, raw_data):
        if isinstance(raw_data, dict):
            raw_data = raw_data.get("code", "")
        raw_str = str(raw_data)
        match = re.search(r"```python(.*?)```", raw_str, re.DOTALL)
        if match:
            return match.group(1).strip()
        match = re.search(r"```(.*?)```", raw_str, re.DOTALL)
        if match:
            return match.group(1).strip()
        return raw_str.strip()

    def execute_python_code(self, code_payload):
        print(f"\n[{self.agent_id}] Extracting and executing Python script...")
        clean_script = self.extract_pure_code(code_payload)
        temp_file = "temp_runner.py"

        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(clean_script)

        try:
            res = subprocess.run(["python3", temp_file], capture_output=True, text=True, timeout=10)
            if res.returncode == 0:
                print(f"[{self.agent_id}] Execution Successful!")
                return {"status": "Success", "stdout": res.stdout}
            else:
                return {"status": "Error", "stdout": res.stderr or "Execution failed"}
        except Exception as e:
            return {"status": "Error", "stdout": str(e)}
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def execute(self, code_payload):
        return self.execute_python_code(code_payload)
