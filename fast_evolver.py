import asyncio
import time
from orchestrator import MasterOrchestrator

async def fast_growth_loop():
    print("\n⚡⚡ [PREM SWARM AI - FAST-EVOLUTION PIPELINE ACTIVATED] ⚡⚡\n")
    master = MasterOrchestrator()

    missions = [
        "Network Speed Tester",
        "System Monitor Engine",
        "JSON Config Parser"
    ]

    print(f"🎯 Scheduled Batch Evolution for {len(missions)} High-Speed Modules...\n")

    for idx, topic in enumerate(missions, 1):
        print(f"\n--- [BATCH STEP {idx}/{len(missions)}: {topic}] ---")
        start_time = time.time()
        await master.run_full_swarm_cycle(topic)
        elapsed = round(time.time() - start_time, 2)
        print(f"⏱️ Module '{topic}' synthesized & saved in {elapsed}s!")

if __name__ == "__main__":
    asyncio.run(fast_growth_loop())
