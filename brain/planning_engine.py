class PlanningEngine:
    def __init__(self):
        print("🎯 [BRAIN Core] Dynamic DAG Planner Active.")

    def decompose_mission(self, mission_topic):
        topic_lower = mission_topic.lower()
        
        if "network" in topic_lower or "http" in topic_lower or "port" in topic_lower:
            domain_tasks = [
                "Protocol Requirement & Socket/HTTP Standard Definition",
                "Timeout & Connection Error Mitigation Strategy",
                "Non-blocking I/O or Async Execution Optimization",
                "Live Endpoint Validation & Exception Boundary Audit"
            ]
        elif "crypto" in topic_lower or "data" in topic_lower or "encrypt" in topic_lower:
            domain_tasks = [
                "Data Schema & Boundary Input Specification",
                "Cryptographic Primitives & Key Management Safety Audit",
                "Algorithmic Performance & Memory Leak Verification",
                "Malformed Payload & Buffer Robustness Testing"
            ]
        else:
            domain_tasks = [
                "Domain Requirement & Target Environment Mapping",
                "Interface Boundary & State Handling Definition",
                "Core Functional Implementation & Edge Case Mitigation",
                "Resource Allocation & Execution Performance Review"
            ]

        subtasks = [{"id": idx + 1, "task": task} for idx, task in enumerate(domain_tasks)]
        return {"mission": mission_topic, "subtasks": subtasks}
