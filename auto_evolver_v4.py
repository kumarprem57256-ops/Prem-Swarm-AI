import os
import sys
import importlib
import asyncio
from orchestrator import MasterOrchestrator

class DynamicEvolutionEngine:
    def __init__(self):
        self.master = MasterOrchestrator()
        self.loaded_modules = {}

    async def evolve_and_load(self, topic):
        print(f"\n🧬 [DYNAMIC EVOLUTION] Triggering rapid build for: '{topic}'...")
        await self.master.run_full_swarm_cycle(topic)

        # Module filename construct karein
        module_name = f"auto_{topic.lower().replace(' ', '_')}"
        filepath = f"{module_name}.py"

        if os.path.exists(filepath):
            try:
                # Add current directory to path
                if os.getcwd() not in sys.path:
                    sys.path.append(os.getcwd())

                # Dynamic Import/Reload
                if module_name in sys.modules:
                    mod = importlib.reload(sys.modules[module_name])
                else:
                    mod = importlib.import_module(module_name)

                self.loaded_modules[topic] = mod
                print(f"🔥 [DYNAMIC HOT-RELOAD SUCCESS] Module '{module_name}' imported into Swarm Runtime!")
                return True
            except Exception as e:
                print(f"❌ [HOT-RELOAD ERROR] Could not dynamically load '{module_name}': {e}")
                return False
        return False

async def main():
    engine = DynamicEvolutionEngine()
    test_topics = ["HTTP Header Checker", "Data Encryption Utility"]
    
    for t in test_topics:
        await engine.evolve_and_load(t)

    print("\n⚡ Dynamic Modules Loaded in Swarm Active Memory:")
    for k, v in engine.loaded_modules.items():
        print(f"  • {k} -> {v}")

if __name__ == "__main__":
    asyncio.run(main())
