import subprocess
import time
import sys

def run_swarm_system():
    print("==================================================")
    print("🚀 LAUNCHING PREM SWARM AI - DEEP LEARNING V4 ENGINE")
    print("==================================================")
    
    print("\n🌐 [1/2] Launching Web Control Dashboard on http://127.0.0.1:5000 ...")
    dashboard_process = subprocess.Popen([sys.executable, "dashboard.py"])
    
    time.sleep(2)
    
    print("\n🧠 [2/2] Launching Deep Learning Evolver V4 Engine...")
    try:
        evolver_process = subprocess.Popen([sys.executable, "auto_evolver_v4.py"])
        evolver_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Swarm Engine and Dashboard...")
        dashboard_process.terminate()
        evolver_process.terminate()
        print("✅ Processes safely stopped.")

if __name__ == "__main__":
    run_swarm_system()
