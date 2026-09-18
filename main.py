import asyncio
from orchestrator import MasterOrchestrator


async def start_swarm():
    print("\n╭─────────────────────────────────────────────╮")
    print("│ PREM SWARM AI: AUTONOMOUS 10-AGENT CORE    │")
    print("╰─────────────────────────────────────────────╯\n")

    master = MasterOrchestrator()

    while True:
        try:
            user_topic = input(
                "\nEnter Swarm Mission Topic (or 'exit' to quit): "
            ).strip()

            if not user_topic:
                continue

            if user_topic.lower() == "exit":
                print("Exiting Swarm Core.")
                break

            print(f"\n🚀 MISSION INITIALIZED: '{user_topic}'")

            # =========================================================
            # AGENT ROUTER DISPATCH
            # =========================================================

            # Research Agent
            try:
                researcher = master.agent_router.route("research")

                research_result = researcher.execute(
                    "research_topic",
                    topic=user_topic
                )

                print(
                    f"🔍 [Research Agent] "
                    f"{researcher.agent_id} completed."
                )

            except Exception as e:
                research_result = None
                print(f"⚠️ [Research Agent] {e}")

            # Business Agent
            try:
                business = master.agent_router.route("business")

                business_result = business.execute(
                    "generate_monetization_plan",
                    business_niche=user_topic
                )

                print(
                    f"💼 [Business Agent] "
                    f"{business.agent_id} completed."
                )

            except Exception as e:
                business_result = None
                print(f"⚠️ [Business Agent] {e}")

            # =========================================================
            # MAIN COGNITIVE SWARM PIPELINE
            # =========================================================

            await master.run_full_swarm_cycle(user_topic)

        except KeyboardInterrupt:
            print("\nShutting down Swarm Core gracefully.")
            break

        except Exception as e:
            print(f"❌ System Error: {e}")


if __name__ == "__main__":
    asyncio.run(start_swarm())
