from typing import Dict, List

class QualityScorer:
    """
    Calculates quality score across multiple dimensions.
    
    Dimensions:
    - Requirement Coverage (requested features implemented)
    - Capability Coverage (planned capabilities implemented)
    - Functional Correctness (exit code, test results)
    - Security (security reviews passed, validation present)
    - Test Coverage (test code present, tests pass)
    - Reliability (error handling, no crashes)
    - Maintainability (code structure, comments, clarity)
    - Performance (execution time, resource usage)
    - Documentation (docstrings, comments, readme)
    
    Does NOT inflate scores just for execution success.
    """
    
    def __init__(self):
        self.agent_id = "QualityScorer-05"
        print(f"📊 [{self.agent_id}] Quality Scoring Engine Initialized.")
    
    def score_quality(self, 
                     code_content: str,
                     sandbox_result: Dict,
                     capability_verifier_result: Dict,
                     critic_result: Dict,
                     security_review: bool,
                     capability_plan: Dict,
                     requirement_expansion: Dict) -> Dict:
        """
        Calculate multi-dimensional quality score.
        
        Returns detailed scoring breakdown with per-dimension scores.
        """
        print(f"\n📊 [{self.agent_id}] Calculating Quality Score...")
        
        # 1. REQUIREMENT COVERAGE
        req_coverage = self._score_requirement_coverage(
            requirement_expansion.get("expected_capabilities", []),
            capability_verifier_result.get("implemented_capabilities", [])
        )
        
        # 2. CAPABILITY COVERAGE  
        cap_coverage = self._score_capability_coverage(capability_verifier_result)
        
        # 3. FUNCTIONAL CORRECTNESS
        func_correct = self._score_functional_correctness(sandbox_result, capability_verifier_result)
        
        # 4. SECURITY
        security_score = self._score_security(security_review, code_content, critic_result)
        
        # 5. TEST COVERAGE
        test_score = self._score_test_coverage(code_content, sandbox_result)
        
        # 6. RELIABILITY
        reliability = self._score_reliability(code_content, sandbox_result)
        
        # 7. MAINTAINABILITY
        maintainability = self._score_maintainability(code_content)
        
        # 8. PERFORMANCE
        performance = self._score_performance(sandbox_result)
        
        # 9. DOCUMENTATION
        documentation = self._score_documentation(code_content)
        
        # WEIGHTED TOTAL (don't just average)
        total_score = (
            req_coverage * 0.15 +
            cap_coverage * 0.15 +
            func_correct * 0.20 +
            security_score * 0.15 +
            test_score * 0.15 +
            reliability * 0.10 +
            maintainability * 0.05 +
            performance * 0.03 +
            documentation * 0.02
        )
        
        scores = {
            "dimensions": {
                "requirement_coverage": round(req_coverage, 1),
                "capability_coverage": round(cap_coverage, 1),
                "functional_correctness": round(func_correct, 1),
                "security": round(security_score, 1),
                "test_coverage": round(test_score, 1),
                "reliability": round(reliability, 1),
                "maintainability": round(maintainability, 1),
                "performance": round(performance, 1),
                "documentation": round(documentation, 1)
            },
            "total_score": round(total_score, 2),
            "score_breakdown": self._explain_scoring(
                req_coverage, cap_coverage, func_correct, security_score,
                test_score, reliability, maintainability, performance, documentation
            ),
            "quality_rating": self._rate_quality(total_score),
            "pass_threshold_met": total_score >= 70.0
        }
        
        print(f"   📊 Total Score: {scores['total_score']}/100")
        print(f"   ⭐ Rating: {scores['quality_rating']}")
        print(f"   ✅ Pass Threshold (≥70): {'YES' if scores['pass_threshold_met'] else 'NO'}")
        
        return scores
    
    def _score_requirement_coverage(self, expected: List[str], implemented: List[str]) -> float:
        """Score what % of requirements are covered."""
        if not expected:
            return 100.0
        
        implemented_lower = [c.lower() for c in implemented]
        covered = sum(1 for exp in expected if any(exp.lower() in impl for impl in implemented_lower))
        
        return (covered / len(expected)) * 100.0
    
    def _score_capability_coverage(self, verifier_result: Dict) -> float:
        """Score based on capability gate results."""
        missing_must = len(verifier_result.get("missing_must_have", []))
        coverage = verifier_result.get("coverage", 0.0)
        
        # Heavy penalty for missing must-haves
        if missing_must > 0:
            return max(0, 50 - (missing_must * 15))
        
        # Otherwise use coverage percentage
        return coverage * 100.0
    
    def _score_functional_correctness(self, sandbox_result: Dict, verifier_result: Dict) -> float:
        """Score based on execution success and capability gate."""
        base_score = 0.0
        
        # Exit code == 0
        if sandbox_result.get("executed_successfully", False):
            base_score += 50.0
        else:
            return 0.0  # Cannot be correct if it crashes
        
        # Capability gate passed
        if verifier_result.get("gate_status") == "PASS":
            base_score += 50.0
        else:
            # Partial credit for some implementation
            base_score += 20.0
        
        return min(100.0, base_score)
    
    def _score_security(self, security_passed: bool, code_content: str, critic_result: Dict) -> float:
        """Score security quality."""
        score = 0.0
        
        if security_passed:
            score += 60.0
        
        # Additional checks
        if "try:" in code_content and "except" in code_content:
            score += 20.0
        
        if "import" in code_content:
            score += 10.0
        
        # Deduct points if critic found issues
        flaws = critic_result.get("flaws", [])
        if flaws:
            score = max(0, score - (len(flaws) * 15))
        
        return min(100.0, score)
    
    def _score_test_coverage(self, code_content: str, sandbox_result: Dict) -> float:
        """Score presence and success of tests."""
        score = 0.0
        
        # Tests present
        if "def test_" in code_content or "run_tests" in code_content:
            score += 40.0
        
        # Tests passed (no errors in execution)
        if sandbox_result.get("exit_code") == 0:
            score += 40.0
        
        # Assertions/checks present
        if "assert" in code_content or "if not " in code_content:
            score += 20.0
        
        return min(100.0, score)
    
    def _score_reliability(self, code_content: str, sandbox_result: Dict) -> float:
        """Score error handling and reliability."""
        score = 0.0
        
        # Error handling present
        if "try:" in code_content and "except" in code_content:
            score += 50.0
        
        # No timeout
        execution_time = sandbox_result.get("execution_time_ms", 5000)
        if execution_time < 5000:
            score += 30.0
        
        # No stderr
        if not sandbox_result.get("stderr", ""):
            score += 20.0
        
        return min(100.0, score)
    
    def _score_maintainability(self, code_content: str) -> float:
        """Score code structure and clarity."""
        score = 50.0  # Base score
        
        # Has classes/functions (structure)
        if "class " in code_content or "def " in code_content:
            score += 20.0
        
        # Has comments/docstrings
        if "\"\"\"" in code_content or "'''" in code_content or "#" in code_content:
            score += 20.0
        
        # Reasonable length (not too long, not too short)
        lines = len(code_content.split("\n"))
        if 10 < lines < 500:
            score += 10.0
        
        return min(100.0, score)
    
    def _score_performance(self, sandbox_result: Dict) -> float:
        """Score execution performance."""
        execution_time = sandbox_result.get("execution_time_ms", 5000)
        
        if execution_time < 100:
            return 100.0
        elif execution_time < 500:
            return 90.0
        elif execution_time < 1000:
            return 75.0
        elif execution_time < 2000:
            return 50.0
        elif execution_time < 5000:
            return 25.0
        else:
            return 0.0
    
    def _score_documentation(self, code_content: str) -> float:
        """Score documentation quality."""
        score = 0.0
        
        # Docstrings
        docstring_count = code_content.count('"""') // 2
        if docstring_count > 0:
            score += 30.0
        
        # Comments
        comment_lines = len([l for l in code_content.split("\n") if "#" in l])
        if comment_lines > 3:
            score += 30.0
        
        # Main block documentation
        if "if __name__" in code_content:
            score += 20.0
        
        # Error messages
        if "print" in code_content or "raise" in code_content:
            score += 20.0
        
        return min(100.0, score)
    
    def _rate_quality(self, score: float) -> str:
        """Convert score to rating."""
        if score >= 90:
            return "EXCELLENT"
        elif score >= 80:
            return "VERY_GOOD"
        elif score >= 70:
            return "GOOD"
        elif score >= 60:
            return "ACCEPTABLE"
        elif score >= 50:
            return "NEEDS_IMPROVEMENT"
        else:
            return "POOR"
    
    def _explain_scoring(self, req, cap, func, sec, test, rel, maint, perf, doc) -> str:
        """Generate score explanation."""
        explanation = []
        
        if req < 70:
            explanation.append(f"⚠️ Requirement coverage low ({req:.0f}%)")
        if cap < 70:
            explanation.append(f"⚠️ Capability coverage low ({cap:.0f}%)")
        if func < 70:
            explanation.append(f"⚠️ Functional correctness issues ({func:.0f}%)")
        if sec < 80:
            explanation.append(f"⚠️ Security score could be higher ({sec:.0f}%)")
        if test < 70:
            explanation.append(f"⚠️ Test coverage needs improvement ({test:.0f}%)")
        
        if not explanation:
            explanation.append("✅ All quality dimensions are acceptable")
        
        return " | ".join(explanation)
