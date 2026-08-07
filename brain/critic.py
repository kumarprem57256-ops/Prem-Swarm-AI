class AdversarialCritic:
    def __init__(self):
        print("🥊 [BRAIN Core] Adversarial Critic Gatekeeper Active.")

    def critique_candidate(self, topic, code_content):
        print(f"🔍 [Critic] Auditing candidate code for '{topic}'...")
        flaws = []
        
        # Static checks for production resilience
        if "try:" not in code_content:
            flaws.append("Missing robust exception handling (try-except blocks).")
        if "import " not in code_content and "from " not in code_content:
            flaws.append("No standard libraries imported.")
            
        score = 100 - (len(flaws) * 25)
        
        return {
            "passed": len(flaws) == 0,
            "flaws": flaws,
            "score": max(score, 0)
        }
