import asyncio
import time
from orchestrator import MasterOrchestrator

async def run_infinite_loop():
    print("🤖 [SWARM AUTOPILOT] Starting Autonomous 24/7 Execution Mode...")
    swarm = MasterOrchestrator()
    
    cycle_count = 1
    while True:
        print(f"\n🔄 --- SWARM ITERATION #{cycle_count} ---")
        try:
            await swarm.run_full_swarm_cycle(trade_symbol="RELIANCE", business_niche="FinTech Automation")
        except Exception as e:
            print(f"❌ Critical Loop Error: {e}. Recovering in 10s...")
        
        cycle_count += 1
        print("💤 Swarm Sleeping for 30 Seconds... (Press CTRL+C to stop)")
        await asyncio.sleep(30)

if __name__ == "__main__":
    try:
        asyncio.run(run_infinite_loop())
    except KeyboardInterrupt:
        print("\n🛑 Swarm Autopilot Safely Terminated by User.")
