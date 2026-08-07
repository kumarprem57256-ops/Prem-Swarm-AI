import re

class IntentEngine:
    def __init__(self):
        print("🧠 [BRAIN Core] Intent Classification Engine Active.")

    def classify_intent(self, user_input):
        text = user_input.strip()
        
        # Command Execution pattern check
        if re.match(r'^(python3?|bash|ls|cd|cat|rm|git)\b', text) or text.endswith('.py'):
            return {"intent": "RUN_COMMAND", "confidence": 0.95, "action": "SYSTEM_EXEC"}

        # Debug/Query pattern check
        if text.lower().startswith(('why', 'how', 'debug', 'explain', 'what')):
            return {"intent": "DEBUG_ANALYSIS", "confidence": 0.88, "action": "LLM_REASONING"}

        # Default Tool Generation
        return {"intent": "CREATE_TOOL", "confidence": 0.90, "action": "FULL_SWARM_PIPELINE"}
