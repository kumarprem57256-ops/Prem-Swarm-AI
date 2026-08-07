import asyncio
from orchestrator import MasterOrchestrator

async def start_swarm():
    print("\n╭─────────────────────────────────────────────╮")
    print("│ PREM SWARM AI: AUTONOMOUS 10-AGENT CORE    │")
    print("╰─────────────────────────────────────────────╯\n")

    master = MasterOrchestrator()

    while True:
        try:
            user_topic = input("\nEnter Swarm Mission Topic (or 'exit' to quit): ").strip()
            if not user_topic:
                continue
            if user_topic.lower() == 'exit':
                print("Exiting Swarm Core.")
                break

            print(f"\n🚀 MISSION INITIALIZED: '{user_topic}'")
            
            master.assign_task("Researcher-01", f"Research insights for '{user_topic}'")
            master.assign_task("Business-02", f"Draft monetization for '{user_topic}'")

            await master.run_full_swarm_cycle(user_topic)

        except KeyboardInterrupt:
            print("\nShutting down Swarm Core gracefully.")
            break
        except Exception as e:
            print(f"❌ System Error: {e}")

if __name__ == "__main__":
    asyncio.run(start_swarm())
