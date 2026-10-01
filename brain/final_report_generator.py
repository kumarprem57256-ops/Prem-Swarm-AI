from typing import Dict, List
import json

class FinalReportGenerator:
    """
    Generates comprehensive final report after mission completion.
    
    Reports:
    - Artifact filename and size
    - Intent classification
    - Requested vs Implemented capabilities
    - Test results
    - Security review results
    - Capability gate result
    - Quality scores (all dimensions)
    - Execution performance
    - Memory/Learning stored
    - Any repair cycles used
    """
    
    def __init__(self):
        self.agent_id = "FinalReportGenerator-06"
        print(f"📄 [{self.agent_id}] Final Report Generation Engine Initialized.")
    
    def generate_final_report(self,
                            request: str,
                            artifact_path: str,
                            intent_result: Dict,
                            requirement_expansion: Dict,
                            capability_plan: Dict,
                            architecture_plan: Dict,
                            code_content: str,
                            sandbox_result: Dict,
                            critic_result: Dict,
                            security_review: bool,
                            capability_verifier_result: Dict,
                            quality_score: Dict,
                            repair_cycles: int,
                            final_status: str) -> Dict:
        """
        Generate comprehensive mission report.
        """
        print(f"\n📄 [{self.agent_id}] Generating Final Report...")
        
        # Calculate artifact metrics
        artifact_size = len(code_content) if code_content else 0
        lines_of_code = len(code_content.split("\n")) if code_content else 0
        
        # Capability summary
        requested_capabilities = requirement_expansion.get("expected_capabilities", [])
        planned_capabilities = capability_plan.get("must_have_capabilities", [])
        implemented_capabilities = capability_verifier_result.get("implemented_capabilities", [])
        tested_capabilities = [c for c in planned_capabilities if not capability_verifier_result.get("missing_must_have", [])]
        
        report = {
            "mission_metadata": {
                "request": request,
                "intent": intent_result.get("intent", "UNKNOWN"),
                "confidence": intent_result.get("confidence", 0),
                "status": final_status,
                "timestamp": self._get_timestamp()
            },
            "artifact": {
                "filename": artifact_path.split("/")[-1] if artifact_path else "NONE",
                "path": artifact_path,
                "size_bytes": artifact_size,
                "lines_of_code": lines_of_code,
                "classes_defined": code_content.count("class ") if code_content else 0,
                "functions_defined": code_content.count("def ") if code_content else 0,
            },
            "capabilities": {
                "requested": requested_capabilities,
                "planned_must_have": planned_capabilities,
                "planned_should_have": capability_plan.get("should_have_capabilities", []),
                "implemented": implemented_capabilities,
                "tested": tested_capabilities,
                "missing": capability_verifier_result.get("missing_must_have", []),
            },
            "capability_gate": {
                "status": capability_verifier_result.get("gate_status", "UNKNOWN"),
                "reason": " | ".join(capability_verifier_result.get("gate_reason", ["Unknown"])),
                "coverage": f"{capability_verifier_result.get('coverage', 0)*100:.1f}%",
                "error_handling_verified": capability_verifier_result.get("error_handling_verified", False),
                "input_validation_verified": capability_verifier_result.get("input_validation_verified", False),
            },
            "testing": {
                "tests_present": "def test_" in code_content or "run_tests" in code_content if code_content else False,
                "exit_code": sandbox_result.get("exit_code", -1),
                "execution_time_ms": sandbox_result.get("execution_time_ms", 0),
                "test_failures": capability_verifier_result.get("test_failures", []),
            },
            "quality": {
                "total_score": quality_score.get("total_score", 0),
                "rating": quality_score.get("quality_rating", "UNKNOWN"),
                "pass_threshold_met": quality_score.get("pass_threshold_met", False),
                "dimensions": quality_score.get("dimensions", {}),
            },
            "security": {
                "security_review_passed": security_review,
                "critic_flaws": critic_result.get("flaws", []),
                "critic_score": critic_result.get("score", 0),
            },
            "repair": {
                "repair_cycles_used": repair_cycles,
                "max_repair_cycles": 3,
            },
            "summary": self._generate_summary(
                final_status,
                capability_verifier_result.get("gate_status", "UNKNOWN"),
                quality_score.get("total_score", 0),
                repair_cycles
            )
        }
        
        return report
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        try:
            from datetime import datetime
            return datetime.now().isoformat()
        except:
            return "timestamp_unavailable"
    
    def _generate_summary(self, final_status: str, gate_status: str, score: float, cycles: int) -> str:
        """Generate human-readable summary."""
        summary_lines = []
        
        if final_status == "PASS":
            summary_lines.append("✅ Mission SUCCESSFUL")
            summary_lines.append(f"   Capability Gate: {gate_status}")
            summary_lines.append(f"   Quality Score: {score}/100")
            if cycles > 1:
                summary_lines.append(f"   Completed after {cycles} repair cycles")
            return "\n".join(summary_lines)
        
        elif final_status == "FAIL":
            summary_lines.append("❌ Mission FAILED")
            if gate_status == "FAIL":
                summary_lines.append("   Reason: Capability Gate did not pass")
            else:
                summary_lines.append(f"   Status: {gate_status}")
            summary_lines.append(f"   Quality Score: {score}/100")
            summary_lines.append(f"   Repair cycles exhausted: {cycles}/3")
            return "\n".join(summary_lines)
        
        else:
            return f"Mission status: {final_status}"
