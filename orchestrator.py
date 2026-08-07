import asyncio
import json
import os

# Safe Dynamic Imports
try:
    from agent_coder import CoderAgent
except ImportError:
    CoderAgent = None

try:
    from agent_executor import ExecutorAgent
except ImportError:
    ExecutorAgent = None

try:
    from agent_media import MediaAgent
except ImportError:
    MediaAgent = None

try:
    from agent_researcher import ResearchAgent
except ImportError:
    ResearchAgent = None

from agent_trading import TradingAgent
from agent_healer import AutoHealerAgent
from agent_business import BusinessAgent


class MasterOrchestrator:
    def __init__(self):
        print("\n⚡ [SWARM MATRIX] Initializing 10-Agent Autonomous Core...")
        
        # Core Specialized Agents Loading
        self.trader = TradingAgent()
        self.healer = AutoHealerAgent()
        self.business = BusinessAgent()
        
        # Optional Agents Integration
        self.coder = CoderAgent() if CoderAgent else None
        self.executor = ExecutorAgent() if ExecutorAgent else None
        self.media = MediaAgent() if MediaAgent else None
        self.researcher = ResearchAgent() if ResearchAgent else None
        
        # System Memory Engine
        self.memory_file = "swarm_brain_memory.json"
        self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r") as f:
                    self.memory = json.load(f)
                print("🧠 [Memory Core] Persistent Memory Loaded.")
            except Exception:
                self.memory = {}
        else:
            self.memory = {}

    async def execute_task_with_healing(self, agent_name, task_func, *args, **kwargs):
        """Auto-Healer wrapper to intercept errors dynamically"""
        try:
            return await task_func(*args, **kwargs)
        except Exception as e:
            print(f"\n⚠️ Failure detected in [{agent_name}]: {e}")
            return await self.healer.diagnose_and_fix(agent_name, str(e), task_func, *args, **kwargs)

    async def run_full_swarm_cycle(self, trade_symbol="RELIANCE", business_niche="FinTech Automation"):
        print("\n=================== 🚀 RUNNING FULL SWARM CYCLE ===================")
        
        # 1. Business Strategy Task
        biz_plan = self.business.generate_monetization_plan(business_niche)
        print(f"📈 [Business Strategy Output]: {biz_plan['strategy']}")

        # 2. Trading Task with Auto-Healing Safety Net
        trade_res = await self.execute_task_with_healing(
            "TradingAgent", 
            self.trader.analyze_and_trade, 
            symbol=trade_symbol, 
            action="BUY", 
            quantity=1
        )
        print(f"💰 [Trading Agent Output]: {trade_res}")

        print("=================== ✅ SWARM CYCLE COMPLETE ===================\n")

if __name__ == "__main__":
    swarm = MasterOrchestrator()
    asyncio.run(swarm.run_full_swarm_cycle())

    def assign_task(self, agent_id, task_description):
        print(f"🤖 [Agent {agent_id}] Executing: {task_description}")
        return f"Task completed by agent {agent_id}"
