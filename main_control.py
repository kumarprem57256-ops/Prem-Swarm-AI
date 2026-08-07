import sys
import os
import asyncio

# Termux Input Buffer Cleaner
def get_clean_input(prompt_text):
    try:
        # Flush standard output buffers before reading input
        sys.stdout.write(prompt_text)
        sys.stdout.flush()
        
        # Read raw line and strip all control whitespace
        user_input = sys.stdin.readline()
        if not user_input:
            return ""
        return user_input.strip()
    except Exception:
        return ""

async def main():
    # Import Orchestrator dynamically after environment setup
    from orchestrator import MasterOrchestrator
    orchestrator = MasterOrchestrator()

    while True:
        # Clear screen buffer lines nicely on Termux
        print("\n" + "="*50)
        print(" [SWARM CONTROL PANEL]")
        print("1. Execute Custom Mission Topic")
        print("2. Run Batch Fast Evolver")
        print("3. Inspect Memory Database")
        print("4. Exit System")
        print("="*50)

        choice = get_clean_input("Select Option (1-4): ")

        if choice == "1":
            topic = get_clean_input("\nEnter Swarm Mission Topic: ")
            if topic:
                await orchestrator.run_full_swarm_cycle(topic)
            else:
                print("⚠️ Blank topic received. Returning to menu.")

        elif choice == "2":
            print("\n🚀 Triggering Batch Fast Evolver...")
            # If fast evolver script exists
            if os.path.exists("fast_evolver.py"):
                os.system("python3 fast_evolver.py")
            else:
                print("⚠️ fast_evolver.py file not found.")

        elif choice == "3":
            print("\n🧠 Inspecting Swarm Memory Core Database...")
            if hasattr(orchestrator, 'memory'):
                try:
                    conn = orchestrator.memory._init_db() or None
                except Exception as e:
                    print(f"Memory inspect error: {e}")

        elif choice == "4":
            print("\n👋 Swarm Control Terminated. Shutdown successful.")
            sys.exit(0)

        else:
            if choice: # Only print if input wasn't empty leftover buffer
                print(f"❌ Invalid choice '{choice}', please enter a valid option (1-4).")

if __name__ == "__main__":
    asyncio.run(main())
