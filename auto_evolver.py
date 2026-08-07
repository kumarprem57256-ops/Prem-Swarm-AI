import asyncio
import random
import time
from orchestrator import MasterOrchestrator

class DigitalHumanEvolver:
    def __init__(self):
        self.orchestrator = MasterOrchestrator()
        self.task_pool = [
            "Market Research on High-Yield Crypto/Stock Trends",
            "Generate B2B Automation Strategy for AI Consulting",
            "Self-Optimize Code Efficiency in Swarm Memory",
            "Search and Summarize Latest AI Agent Frameworks"
        ]
        self.completed_tasks = []

    def discover_next_task(self):
        """Self-Task Discovery Engine"""
        # Selects or generates new goal based on past execution
        available_tasks = [t for t in self.task_pool if t not in self.completed_tasks]
        if not available_tasks:
            # Refresh Task Pool with dynamic objectives
            self.task_pool.append(f"Autonomous Research Goal #{len(self.completed_tasks) + 1}")
            available_tasks = [self.task_pool[-1]]
        
        selected_task = random.choice(available_tasks)
        return selected_task

    async def execute_autonomous_life_cycle(self):
        print("\n🧠 [DIGITAL HUMAN AGENT] Initializing Self-Discovery & Autonomous Loop...")
        
        cycle = 1
        while True:
            print(f"\n⚡ --- AUTONOMOUS TASK CYCLE #{cycle} ---")
            
            # 1. Discover New Task
            current_task = self.discover_next_task()
            print(f"🎯 [Autonomous Goal Identified]: {current_task}")
            
            # 2. Assign & Execute via Master Orchestrator
            try:
                print(f"⚙️ [Executing Task via Swarm Matrix]...")
                if "Market" in current_task or "Stock" in current_task:
                    await self.orchestrator.run_full_swarm_cycle(trade_symbol="NIFTY50", business_niche="FinTech")
                else:
                    await self.orchestrator.run_full_swarm_cycle(trade_symbol="RELIANCE", business_niche="SaaS Automation")
                
                self.completed_tasks.append(current_task)
                print(f"✅ [Task Mastered & Logged]: {current_task}")
                
            except Exception as e:
                print(f"🚨 [Execution Issue Intercepted]: {e}")
            
            cycle += 1
            print("💤 [Agent Thinking & Self-Optimizing... Sleeping 15s]")
            await asyncio.sleep(15)

if __name__ == "__main__":
    agent = DigitalHumanEvolver()
    asyncio.run(agent.execute_autonomous_life_cycle())
