import os

class ReviewerAgent:
    def __init__(self):
        self.agent_id = "Reviewer-03"
        self.forbidden_patterns = ["os.remove('/')", "rm -rf", "subprocess.call('rm'", "sys.exit()"]

    def review_code(self, code_content):
        print(f"🧐 [{self.agent_id}] Scanning code for security risks...")
        
        # Check for dangerous patterns
        for pattern in self.forbidden_patterns:
            if pattern in code_content:
                print(f"❌ [{self.agent_id}] SECURITY ALERT: Dangerous pattern found: {pattern}")
                return False
        
        # Check if it imports standard Swarm modules
        if "from orchestrator" not in code_content and "def main" not in code_content:
            print(f"⚠️ [{self.agent_id}] Warning: Code structure might be unstable.")
            
        print(f"✅ [{self.agent_id}] Security Review Passed.")
        return True
