import os
import requests

class BusinessAgent:
    def __init__(self):
        self.agent_id = "Business-02"
        self.groq_api_key = os.getenv("GROQ_API_KEY", "").strip()

    def generate_monetization_plan(self, business_niche):
        print(f"💼 [{self.agent_id}] Groq AI Synthesizing Business Strategy for: '{business_niche}'...")

        if not self.groq_api_key:
            return "Mock Strategy: Set subscription tier at $29/mo."

        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Android; Mobile)"
        }

        prompt = f"Create a concise, high-converting monetization framework for a tech product named '{business_niche}'. Include: 1. Target Audience, 2. Revenue Model (SaaS/Tiered), 3. Key Value Proposition. Keep under 150 words."

        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are a senior SaaS Business Growth Executive."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.4,
            "max_tokens": 300
        }

        try:
            res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=15)
            if res.status_code == 200:
                return res.json()['choices'][0]['message']['content'].strip()
            return "Error generating live strategy."
        except Exception as e:
            return f"Business Strategy Error: {e}"
