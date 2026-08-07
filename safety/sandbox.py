import subprocess
import time
import sys

class ExecutionSandbox:
    def __init__(self):
        print("🛡️ [SAFETY Core] Empirical Execution Sandbox Initialized.")

    def Execute_and_benchmark(self, script_path):
        print(f"🧪 [Sandbox] Running empirical runtime benchmark on '{script_path}'...")
        start_time = time.time()
        
        try:
            # Subprocess execution in isolated environment with strict timeout
            process = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            elapsed_ms = (time.time() - start_time) * 1000
            
            success = (process.returncode == 0)
            print(f"⏱️ [Sandbox Result] Exit Code: {process.returncode} | Execution Time: {elapsed_ms:.2f}ms")
            
            return {
                "executed_successfully": success,
                "exit_code": process.returncode,
                "execution_time_ms": elapsed_ms,
                "stdout": process.stdout[:200],
                "stderr": process.stderr[:200]
            }
        except subprocess.TimeoutExpired:
            print("❌ [Sandbox Result] Process TIMED OUT (>5000ms). Execution terminated.")
            return {
                "executed_successfully": False,
                "exit_code": -1,
                "execution_time_ms": 5000,
                "stdout": "",
                "stderr": "Execution Timeout Expired"
            }
        except Exception as e:
            return {
                "executed_successfully": False,
                "exit_code": 1,
                "execution_time_ms": 0,
                "stdout": "",
                "stderr": str(e)
            }
