import re
from typing import Dict, List, Set

class RequirementExpander:
    """
    Converts user request into structured requirement specifications.
    
    Example:
        Input: "build a data entry agent"
        Output: {
            "core_requirements": [...],
            "expected_capabilities": [...],
            "error_cases": [...],
            "testing_requirements": [...]
        }
    """
    
    def __init__(self):
        self.request_patterns = {
            "agent": ["record creation", "record retrieval", "filtering", "updating", "deletion", "decision making", "task execution"],
            "data": ["import", "export", "validation", "transformation", "cleaning", "persistence", "schema"],
            "api": ["endpoint handling", "request validation", "response formatting", "authentication", "rate limiting", "error responses"],
            "tool": ["core functionality", "error handling", "logging", "configuration", "testing", "documentation"],
            "website": ["routing", "templating", "static assets", "error handling", "responsive design"],
            "calculator": ["input validation", "computation accuracy", "edge cases", "error handling", "clear interface"],
            "database": ["create", "read", "update", "delete", "indexing", "transactions", "backup"],
            "security": ["validation", "sanitization", "encryption", "authentication", "access control", "audit logging"],
            "ai": ["model loading", "inference", "error handling", "caching", "performance optimization"],
        }
    
    def expand(self, user_request: str) -> Dict:
        """
        Parse and expand user request into structured requirements.
        """
        request_lower = user_request.lower()
        
        # 1. CORE REQUIREMENTS
        core_reqs = self._extract_core_requirements(user_request)
        
        # 2. EXPECTED CAPABILITIES (inferred from request patterns)
        capabilities = self._infer_capabilities(request_lower)
        
        # 3. INPUTS & OUTPUTS
        io_spec = self._infer_io_spec(request_lower, user_request)
        
        # 4. ERROR CASES
        error_cases = self._identify_error_cases(request_lower, capabilities)
        
        # 5. SECURITY REQUIREMENTS
        security_reqs = self._identify_security_requirements(request_lower, capabilities)
        
        # 6. PERSISTENCE REQUIREMENTS
        persistence_reqs = self._identify_persistence_requirements(request_lower)
        
        # 7. TESTING REQUIREMENTS
        testing_reqs = self._identify_testing_requirements(capabilities, error_cases)
        
        # 8. USABILITY REQUIREMENTS
        usability_reqs = self._identify_usability_requirements(request_lower)
        
        # 9. PERFORMANCE CONSIDERATIONS
        performance_reqs = self._identify_performance_requirements(request_lower)
        
        # 10. DOCUMENTATION REQUIREMENTS
        doc_reqs = self._identify_documentation_requirements()
        
        return {
            "original_request": user_request,
            "core_requirements": core_reqs,
            "expected_capabilities": capabilities,
            "inputs_outputs": io_spec,
            "error_cases": error_cases,
            "security_requirements": security_reqs,
            "persistence_requirements": persistence_reqs,
            "testing_requirements": testing_reqs,
            "usability_requirements": usability_reqs,
            "performance_considerations": performance_reqs,
            "documentation_requirements": doc_reqs,
            "complexity_estimate": self._estimate_complexity(capabilities)
        }
    
    def _extract_core_requirements(self, request: str) -> List[str]:
        """Extract primary objectives from request."""
        core = []
        
        request_lower = request.lower()
        
        # Identify primary object
        if "agent" in request_lower:
            core.append("Autonomous task execution")
        if "tool" in request_lower or "utility" in request_lower:
            core.append("Focused functionality delivery")
        if "api" in request_lower or "endpoint" in request_lower:
            core.append("HTTP/REST interface")
        if "database" in request_lower or "storage" in request_lower:
            core.append("Data persistence layer")
        if "security" in request_lower or "encrypt" in request_lower or "auth" in request_lower:
            core.append("Security/Access control")
        if "calculator" in request_lower or "compute" in request_lower:
            core.append("Accurate computation")
        if "monitor" in request_lower or "track" in request_lower:
            core.append("Real-time monitoring/tracking")
        
        # Extract key verbs
        verbs = ["build", "create", "design", "implement", "develop", "generate"]
        for verb in verbs:
            if verb in request_lower:
                # Extract noun phrase after verb
                match = re.search(rf"{verb}\s+(?:a\s+)?([^.!?]+?)(?:\s+(?:for|that|which|with)|$)", request, re.IGNORECASE)
                if match:
                    core.append(f"{verb.capitalize()}: {match.group(1).strip()}")
                    break
        
        return core if core else ["Implement requested functionality"]
    
    def _infer_capabilities(self, request_lower: str) -> List[str]:
        """Infer what capabilities should be implemented."""
        capabilities = set()
        
        # Type-based inference
        for type_key, type_caps in self.request_patterns.items():
            if type_key in request_lower:
                capabilities.update(type_caps)
        
        # Verb-based inference
        if any(w in request_lower for w in ["read", "get", "fetch", "retrieve", "query"]):
            capabilities.add("Data retrieval")
        if any(w in request_lower for w in ["write", "save", "store", "create", "add"]):
            capabilities.add("Data creation/writing")
        if any(w in request_lower for w in ["update", "modify", "edit", "change"]):
            capabilities.add("Data modification")
        if any(w in request_lower for w in ["delete", "remove"]):
            capabilities.add("Data deletion")
        if any(w in request_lower for w in ["filter", "search", "query", "find"]):
            capabilities.add("Filtering/searching")
        if any(w in request_lower for w in ["validate", "verify", "check"]):
            capabilities.add("Input validation")
        if any(w in request_lower for w in ["log", "track", "audit", "monitor"]):
            capabilities.add("Logging/auditing")
        if any(w in request_lower for w in ["test", "check", "verify"]):
            capabilities.add("Testing/verification")
        
        # Default capabilities for all
        capabilities.add("Error handling")
        capabilities.add("Proper exit codes")
        
        return sorted(list(capabilities))
    
    def _infer_io_spec(self, request_lower: str, request: str) -> Dict:
        """Infer input/output specifications."""
        return {
            "inputs": self._infer_inputs(request_lower, request),
            "outputs": self._infer_outputs(request_lower, request),
            "interface": self._infer_interface(request_lower)
        }
    
    def _infer_inputs(self, request_lower: str, request: str) -> List[str]:
        """Infer what inputs the tool should accept."""
        inputs = []
        
        if "agent" in request_lower:
            inputs.extend(["Task description", "Configuration parameters"])
        if "data" in request_lower:
            inputs.extend(["Data file/source", "Transformation parameters"])
        if "api" in request_lower:
            inputs.extend(["HTTP request", "Query/body parameters"])
        if "database" in request_lower:
            inputs.extend(["Record data", "Query filters"])
        if "calculator" in request_lower:
            inputs.extend(["Numeric operands", "Operation type"])
        if "security" in request_lower or "encrypt" in request_lower:
            inputs.extend(["Data to secure", "Security key/credential"])
        
        return inputs if inputs else ["User input", "Configuration"]
    
    def _infer_outputs(self, request_lower: str, request: str) -> List[str]:
        """Infer what outputs should be produced."""
        outputs = []
        
        if "agent" in request_lower:
            outputs.extend(["Task result", "Execution log"])
        if "data" in request_lower:
            outputs.extend(["Transformed data", "Validation report"])
        if "api" in request_lower:
            outputs.extend(["JSON response", "HTTP status"])
        if "database" in request_lower:
            outputs.extend(["Record/query result", "Operation confirmation"])
        if "calculator" in request_lower:
            outputs.extend(["Numeric result", "Computation steps"])
        if "security" in request_lower or "encrypt" in request_lower:
            outputs.extend(["Secured/verified data", "Status confirmation"])
        if "log" in request_lower or "report" in request_lower or "summary" in request_lower:
            outputs.extend(["Detailed report", "Summary statistics"])
        
        return outputs if outputs else ["Result/status", "Logging output"]
    
    def _infer_interface(self, request_lower: str) -> str:
        """Infer primary interface type."""
        if "api" in request_lower or "http" in request_lower or "rest" in request_lower or "endpoint" in request_lower:
            return "HTTP API"
        if "cli" in request_lower or "command" in request_lower or "terminal" in request_lower:
            return "Command-line interface"
        if "web" in request_lower or "site" in request_lower or "website" in request_lower:
            return "Web application"
        if "database" in request_lower or "db" in request_lower:
            return "Database interface"
        if "library" in request_lower or "module" in request_lower or "sdk" in request_lower:
            return "Python library/module"
        return "Programmatic interface"
    
    def _identify_error_cases(self, request_lower: str, capabilities: List[str]) -> List[str]:
        """Identify important error scenarios to handle."""
        errors = [
            "Empty/null inputs",
            "Invalid input types/formats",
            "Out-of-range values"
        ]
        
        if "database" in request_lower or "storage" in request_lower or "file" in request_lower:
            errors.extend(["File not found", "Database connection failure", "Disk full/write error"])
        
        if "network" in request_lower or "api" in request_lower or "http" in request_lower:
            errors.extend(["Network timeout", "Connection refused", "Invalid response format"])
        
        if "calculate" in request_lower or "compute" in request_lower:
            errors.extend(["Division by zero", "Overflow", "Precision loss"])
        
        if "security" in request_lower or "encrypt" in request_lower:
            errors.extend(["Invalid credentials", "Decryption failure", "Unauthorized access"])
        
        if any(cap in " ".join(capabilities).lower() for cap in ["data retrieval", "filtering"]):
            errors.append("No results found")
        
        return errors
    
    def _identify_security_requirements(self, request_lower: str, capabilities: List[str]) -> List[str]:
        """Identify security considerations."""
        reqs = ["Input validation", "Error messages without sensitive info"]
        
        if "auth" in request_lower or "password" in request_lower or "credential" in request_lower or "security" in request_lower:
            reqs.extend(["Secure credential handling", "Access control validation"])
        
        if "encrypt" in request_lower or "crypto" in request_lower or "secure" in request_lower:
            reqs.extend(["Use secure algorithms", "Proper key management"])
        
        if "database" in request_lower or "data" in request_lower:
            reqs.extend(["SQL injection prevention", "Data sanitization"])
        
        if "api" in request_lower or "http" in request_lower:
            reqs.extend(["HTTPS consideration", "CORS handling"])
        
        if "file" in request_lower or "storage" in request_lower:
            reqs.append("File path traversal prevention")
        
        return reqs
    
    def _identify_persistence_requirements(self, request_lower: str) -> List[str]:
        """Identify data persistence needs."""
        if "database" in request_lower or "storage" in request_lower:
            return ["SQLite database", "CRUD operations", "Data consistency"]
        
        if "file" in request_lower or "save" in request_lower or "load" in request_lower:
            return ["File I/O", "Serialization format", "Error recovery"]
        
        if "cache" in request_lower or "memory" in request_lower:
            return ["In-memory caching", "TTL management"]
        
        if "agent" in request_lower or "state" in request_lower:
            return ["State persistence", "Recovery mechanism"]
        
        return []  # Stateless operations
    
    def _identify_testing_requirements(self, capabilities: List[str], error_cases: List[str]) -> List[str]:
        """Identify testing strategy."""
        tests = [
            f"Happy path test for each capability",
            f"Error handling for: {', '.join(error_cases[:3])}",
            "Input validation tests",
            "Boundary/edge case tests"
        ]
        
        if any("persistence" in cap.lower() or "database" in cap.lower() or "file" in cap.lower() for cap in capabilities):
            tests.append("Data persistence verification")
        
        if any("api" in cap.lower() or "http" in cap.lower() for cap in capabilities):
            tests.append("Response format validation")
        
        if any("security" in cap.lower() or "encrypt" in cap.lower() for cap in capabilities):
            tests.append("Security constraint tests")
        
        tests.append("Execution completes without hanging/timeout")
        
        return tests
    
    def _identify_usability_requirements(self, request_lower: str) -> List[str]:
        """Identify usability expectations."""
        reqs = ["Clear error messages", "Reasonable execution time"]
        
        if "api" in request_lower or "http" in request_lower:
            reqs.extend(["Clear endpoint documentation", "Consistent response format"])
        
        if "cli" in request_lower or "command" in request_lower:
            reqs.extend(["Clear command usage", "Help documentation"])
        
        if "web" in request_lower or "site" in request_lower:
            reqs.extend(["Responsive layout", "Intuitive navigation"])
        
        if "agent" in request_lower or "tool" in request_lower:
            reqs.append("Simple configuration")
        
        return reqs
    
    def _identify_performance_requirements(self, request_lower: str) -> List[str]:
        """Identify performance targets."""
        reqs = ["Should complete in reasonable time", "No memory leaks"]
        
        if "data" in request_lower or "large" in request_lower or "bulk" in request_lower:
            reqs.append("Handle data sets efficiently")
        
        if "real-time" in request_lower or "stream" in request_lower:
            reqs.append("Low latency")
        
        if "api" in request_lower:
            reqs.append("Response time < 1000ms typical")
        
        return reqs
    
    def _identify_documentation_requirements(self) -> List[str]:
        """Standard documentation requirements."""
        return [
            "Code comments for complex logic",
            "Docstrings for functions/classes",
            "README or usage guide",
            "Example usage"
        ]
    
    def _estimate_complexity(self, capabilities: List[str]) -> str:
        """Estimate task complexity from capability count."""
        count = len(capabilities)
        if count <= 2:
            return "MINIMAL"
        elif count <= 5:
            return "LOW"
        elif count <= 8:
            return "MEDIUM"
        elif count <= 12:
            return "HIGH"
        else:
            return "VERY_HIGH"
