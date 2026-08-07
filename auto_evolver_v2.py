import asyncio
import sqlite3
import json
import urllib.request
import urllib.parse
import re
from datetime import datetime
from orchestrator import MasterOrchestrator

# ==========================================
# 1. SQLITE PERSISTENT EXECUTION MEMORY
# ==========================================
class SwarmMemoryDB:
    def __init__(self, db_name="swarm_execution_memory.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_description TEXT,
                category TEXT,
                status TEXT,
                result TEXT,
                timestamp TEXT
            )
        ''')
        self.conn.commit()

    def log_task(self, task, category, status, result):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO task_history (task_description, category, status, result, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (task, category, status, str(result), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()

    def get_past_tasks(self, limit=5):
        cursor = self.conn.cursor()
        cursor.execute('SELECT task_description, status FROM task_history ORDER BY id DESC LIMIT ?', (limit,))
        return cursor.fetchall()


# ==========================================
# 2. REAL-TIME WEB SCRAPER & RESEARCHER (FIXED)
# ==========================================
class WebResearcher:
    def fetch_live_news(self, query="latest AI agent developments"):
        print(f"🌐 [Web Scraper] Fetching live web insights for: '{query}'...")
        try:
            url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                html = response.read().decode('utf-8', errors='ignore')
                
                # Dynamic extraction for DDG text snippets
                snippets = re.findall(r'<a class="result__snippet[^>]*>(.*?)</a>', html, re.DOTALL)
                if not snippets:
                    snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</td>', html, re.DOTALL)
                
                clean_snippets = [re.sub(r'<[^>]+>', '', s).strip() for s in snippets[:3] if s.strip()]
                return clean_snippets if clean_snippets else ["Live web parsing completed."]
        except Exception as e:
            return [f"Web Scraper Notice: Running in fallback mode ({e})"]


# ==========================================
# 3. DYNAMIC GOAL GENERATOR & EVOLVER
# ==========================================
class DynamicEvolver:
    def __init__(self):
        self.orchestrator = MasterOrchestrator()
        self.db = SwarmMemoryDB()
        self.scraper = WebResearcher()

    def generate_dynamic_goal(self):
        categories = ["FinTech Automation", "SaaS Strategy", "Market Analysis", "Code Efficiency"]
        timestamp_id = int(datetime.now().timestamp()) % len(categories)
        selected_category = categories[timestamp_id]
        generated_task = f"Autonomous Deep Dive: {selected_category} Goal #{int(datetime.now().timestamp()) % 100}"
        return generated_task, selected_category

    async def run_autonomous_loop(self):
        print("\n🚀 [SWARM EVOLVER V2] Active | Dynamic Goals + Web Scraper + SQLite Memory")
        
        cycle = 1
        while True:
            print(f"\n⚡ ================= ITERATION #{cycle} =================")
            
            # 1. Dynamic Goal Generation
            task, category = self.generate_dynamic_goal()
            print(f"🎯 [Dynamic Goal Generated]: {task}")
            print(f"🏷️ [Category]: {category}")

            # 2. Real-Time Web Scraping
            insights = self.scraper.fetch_live_news(f"{category} trends")
            print(f"🔍 [Web Insights Retrieved]: {insights[0] if insights else 'None'}")

            # 3. Orchestrated Swarm Execution
            try:
                print("⚙️ [Executing Task via Swarm Orchestrator]...")
                if "FinTech" in category or "Market" in category:
                    res = await self.orchestrator.run_full_swarm_cycle(trade_symbol="NIFTY50", business_niche=category)
                else:
                    res = await self.orchestrator.run_full_swarm_cycle(trade_symbol="RELIANCE", business_niche=category)

                # 4. Log Result to SQLite Memory DB
                self.db.log_task(task, category, "SUCCESS", "Executed without errors")
                print(f"💾 [SQLite DB] Task logged to 'swarm_execution_memory.db'.")

            except Exception as e:
                print(f"🚨 [Error Intercepted]: {e}")
                self.db.log_task(task, category, "FAILED", str(e))

            cycle += 1
            print("💤 [Swarm Thinking & Self-Optimizing... Sleeping 15s]")
            await asyncio.sleep(15)

if __name__ == "__main__":
    evolver = DynamicEvolver()
    asyncio.run(evolver.run_autonomous_loop())
