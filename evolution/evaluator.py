class SystemEvaluator:
    def __init__(self):
        print("📊 [EVOLUTION] Empirical Score Engine Active.")

    def evaluate_build(self, sandbox_results, critic_results, security_passed):
        # 1. Correctness (30%): Subprocess Exit Code
        correctness = 100 if sandbox_results["executed_successfully"] else 0

        # 2. Reliability (20%): Critic Analysis Score
        reliability = critic_results.get("score", 0)

        # 3. Security (15%): Static Review Pass
        security = 100 if security_passed else 0

        # 4. Efficiency (15%): Execution Latency Under 1000ms
        latency = sandbox_results.get("execution_time_ms", 5000)
        efficiency = max(0, min(100, int(100 - (latency / 20))))

        # 5. Coverage & Reasoning (20%): Stdout/Stderr Verification
        reasoning = 100 if sandbox_results["stderr"] == "" else 30
        coverage = 80 if sandbox_results["stdout"] != "" else 40

        total_score = (
            (correctness * 0.30) +
            (reliability * 0.20) +
            (security * 0.15) +
            (efficiency * 0.15) +
            (coverage * 0.10) +
            (reasoning * 0.10)
        )

        return {
            "total_score": round(total_score, 2),
            "status": "PASS" if total_score >= 70 and correctness == 100 else "REJECT_ROLLBACK",
            "metrics": {
                "correctness": correctness,
                "reliability": reliability,
                "security": security,
                "efficiency": efficiency
            }
        }
