class FailureAnalyzer:
    def __init__(self):
        print("🔍 [BRAIN Core] Empirical Failure Analyzer Active.")

    def analyze_failure(self, sandbox_results):
        stderr = sandbox_results.get("stderr", "")
        exit_code = sandbox_results.get("exit_code", 0)

        if exit_code == -1:
            error_type = "EXECUTION_TIMEOUT"
            summary = "The script timed out (>5000ms). Cause: Unbounded input read (e.g. sys.stdin.read()) without EOF or blocking loop. Ensure self-tests do not wait for interactive stdin input."
        elif "ModuleNotFoundError" in stderr:
            error_type = "MISSING_DEPENDENCY"
            summary = stderr[-300:]
        elif "SyntaxError" in stderr:
            error_type = "SYNTAX_ERROR"
            summary = stderr[-300:]
        else:
            error_type = "RUNTIME_CRASH"
            summary = stderr[-300:] if stderr else "Non-zero exit code"

        print(f"🩹 [Failure Analyzer] Classification: {error_type} | Exit Code: {exit_code}")
        return {
            "error_type": error_type,
            "traceback_summary": summary
        }
