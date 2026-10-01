from typing import Dict, List, Tuple

class CapabilityPlanner:
    """
    Creates internal capability checklist before coding.
    
    For a request, determines:
    - What capabilities MUST be implemented
    - What capabilities are SHOULD-HAVE
    - What capabilities are NICE-TO-HAVE
    
    The Capability Gate will later verify these are actually implemented.
    """
    
    def __init__(self):
        self.agent_id = "CapabilityPlanner-01"
        print(f"📋 [{self.agent_id}] Capability Planning Engine Initialized.")
    
    def plan_capabilities(self, request: str, expanded_requirements: Dict) -> Dict:
        """
        Create capability plan from expanded requirements.
        
        Returns capability checklist with priority levels.
        """
        print(f"\n🎯 [{self.agent_id}] Planning Capabilities for: '{request[:60]}...'")
        
        expected_caps = expanded_requirements.get("expected_capabilities", [])
        complexity = expanded_requirements.get("complexity_estimate", "MEDIUM")
        
        # Categorize capabilities by priority
        must_have = []
        should_have = []
        nice_to_have = []
        
        for cap in expected_caps:
            if self._is_critical(cap, request):
                must_have.append(cap)
            elif self._is_important(cap, request):
                should_have.append(cap)
            else:
                nice_to_have.append(cap)
        
        # Add standard requirements
        if "Error handling" not in must_have:
            must_have.insert(0, "Error handling")
        if "Input validation" not in must_have:
            must_have.insert(0, "Input validation")
        
        plan = {
            "request": request,
            "complexity": complexity,
            "must_have_capabilities": must_have,
            "should_have_capabilities": should_have,
            "nice_to_have_capabilities": nice_to_have,
            "total_capabilities": len(must_have) + len(should_have) + len(nice_to_have),
            "required_capabilities": len(must_have),
            "testing_priority": self._determine_testing_priority(must_have, should_have)
        }
        
        print(f"   📌 Must-Have ({len(must_have)}): {', '.join(must_have[:3])}{'...' if len(must_have) > 3 else ''}")
        print(f"   📌 Should-Have ({len(should_have)}): {', '.join(should_have[:2])}{'...' if len(should_have) > 2 else ''}")
        
        return plan
    
    def _is_critical(self, capability: str, request: str) -> bool:
        """Determine if capability is MUST-HAVE."""
        critical_keywords = [
            "error handling", "input validation", "data creation",
            "core functionality", "decision making"
        ]
        
        cap_lower = capability.lower()
        for kw in critical_keywords:
            if kw in cap_lower:
                return True
        
        # If request specifically mentions the capability, it's critical
        if capability.lower() in request.lower():
            return True
        
        return False
    
    def _is_important(self, capability: str, request: str) -> bool:
        """Determine if capability is SHOULD-HAVE."""
        important_keywords = [
            "retrieval", "filtering", "modification", "deletion",
            "testing", "logging", "documentation"
        ]
        
        cap_lower = capability.lower()
        for kw in important_keywords:
            if kw in cap_lower:
                return True
        
        return False
    
    def _determine_testing_priority(self, must_have: List[str], should_have: List[str]) -> List[str]:
        """Determine testing priority order."""
        priority = []
        
        # Test must-have capabilities first
        for cap in must_have:
            priority.append(f"test_{cap.lower().replace(' ', '_').replace('/', '_')}")
        
        # Then should-have
        for cap in should_have[:3]:  # Limit to top 3
            priority.append(f"test_{cap.lower().replace(' ', '_').replace('/', '_')}")
        
        return priority
