import os, sys, subprocess, requests, json, time, hashlib, threading, random, re

MEMORY_FILE = "swarm_brain_memory.json"

class FileCreatorTool:
    @staticmethod
    def write_file(filepath, content):
        try:
            folder = os.path.dirname(filepath)
            if folder and not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return f"✅ File created: `{filepath}`"
        except Exception as e:
            return f"❌ [FILE ERROR]: {str(e)}"

class SystemActionTool:
    @staticmethod
    def execute_terminal_cmd(command):
        blocked = ["rm -rf /", "mkfs", "dd"]
        for b in blocked:
            if b in command:
                return "⚠️ [SECURITY RISK] Command blocked."
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=10)
            return output.decode('utf-8').strip()
        except Exception as e:
            return f"❌ [EXECUTION ERROR]: {str(e)}"

class SmartVectorMemory:
    def __init__(self):
        self.memory = {}
        self.load_memory()

    def load_memory(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f:
                    self.memory = json.load(f)
            except Exception:
                self.memory = {}

    def get_keywords(self, text):
        words = re.findall(r'\w+', text.lower())
        stopwords = {'is', 'the', 'a', 'an', 'and', 'or', 'to', 'in', 'of', 'for', 'with', 'on', 'at', 'me', 'ko', 'ka', 'ki', 'se', 'hai'}
        return {w for w in words if w not in stopwords and len(w) > 2}

    def search_knowledge(self, query, threshold=0.40):
        query_words = self.get_keywords(query)
        if not query_words:
            return None
        best_match = None
        highest_score = 0.0
        for item in self.memory.values():
            saved_words = self.get_keywords(item.get("query", ""))
            intersection = len(query_words.intersection(saved_words))
            union = len(query_words.union(saved_words))
            score = intersection / float(union) if union > 0 else 0
            if score > highest_score:
                highest_score = score
                best_match = item
        if highest_score >= threshold:
            return best_match
        return None

    def learn_knowledge(self, query, response, source="Swarm_Core"):
        q_hash = hashlib.md5(query.lower().strip().encode()).hexdigest()
        self.memory[q_hash] = {
            "query": query,
            "response": response,
            "learned_from": source,
            "timestamp": time.time()
        }
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memory, f, indent=2)

class GeminiTeacherEngine:
    def __init__(self, api_key):
        self.api_key = api_key

    def query(self, prompt, system_instruction):
        if not self.api_key:
            return "❌ [API KEY MISSING]: GEMINI_API_KEY environment variable is empty."

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "systemInstruction": {"parts": [{"text": system_instruction}]}
        }

        # Gemini 2.0 Flash Endpoint
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=25)
            if res.status_code == 200:
                data = res.json()
                try:
                    return data["candidates"][0]["content"]["parts"][0]["text"]
                except (KeyError, IndexError):
                    return f"⚠️ [PARSE ERROR]: {json.dumps(data)}"
            else:
                return f"❌ [GEMINI API ERROR]: HTTP {res.status_code}: {res.text}"
        except Exception as e:
            return f"❌ [CONNECTION ERROR]: {str(e)}"

class MultiAgentSwarmOrchestrator:
    def __init__(self, teacher_engine):
        self.teacher = teacher_engine

    def execute_swarm_task(self, task_description):
        print("\n🧩 [AGENT 1: PLANNER] Break down logic initiated...")
        plan = self.teacher.query(
            f"Break down this goal into clear execution steps: {task_description}",
            "You are PLANNER AGENT. Give sharp, structured architectural steps."
        )

        print("🔬 [AGENT 2: RESEARCHER] Generating specs...")
        specs = self.teacher.query(
            f"Based on this plan: '{plan}', provide exact technical logic, parameters, and algorithms needed.",
            "You are RESEARCHER AGENT. Focus on deep code specs and logic."
        )

        print("💻 [AGENT 3: CODER] Building final code solution...")
        code_solution = self.teacher.query(
            f"Implement clean production Python code based on these specs:\n{specs}",
            "You are CODER AGENT. Output only functional, production-ready code."
        )

        return f"""👑 **[NEXUS MULTI-AGENT SWARM WORKFLOW]**

📋 **[AGENT 1 - PLANNER ROADMAP]**
{plan}

---
🔬 **[AGENT 2 - TECHNICAL SPECS]**
{specs}

---
💻 **[AGENT 3 - CODER EXECUTION]**
{code_solution}"""

class NexusAICore:
    def __init__(self, callback_func=None, api_key=None):
        self.callback_func = callback_func
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.memory = SmartVectorMemory()
        self.teacher = GeminiTeacherEngine(self.api_key)
        self.swarm = MultiAgentSwarmOrchestrator(self.teacher)

    def process_user_input(self, user_msg):
        clean_msg = user_msg.strip()

        if clean_msg.startswith("cmd:"):
            return SystemActionTool.execute_terminal_cmd(clean_msg.replace("cmd:", "").strip())

        if clean_msg.startswith("swarm:"):
            return self.swarm.execute_swarm_task(clean_msg.replace("swarm:", "").strip())

        cached = self.memory.search_knowledge(clean_msg)
        if cached:
            return f"🧠 **[MEMORY CORE]**\n{cached['response']}"

        response = self.teacher.query(clean_msg, "You are NEXUS ARCHITECT AI built by Prem.")
        if response and "❌" not in response:
            self.memory.learn_knowledge(clean_msg, response)
        return response

    def start_thought_loop(self):
        pass

LocalOllamaBrain = NexusAICore

if __name__ == "__main__":
    ai = NexusAICore()
    print("🤖 MULTI-AGENT SWARM BRAIN UPDATED TO GEMINI 2.0 FLASH!")
