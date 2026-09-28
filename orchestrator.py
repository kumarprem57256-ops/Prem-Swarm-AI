import os
import asyncio
from agent_business import BusinessAgent
from agent_coder import CoderAgent
from agent_reviewer import ReviewerAgent
from memory.memory_core import MemoryCore

from brain.utils import validate_and_clean_input, generate_tool_name
from brain.intent_engine import IntentEngine
from brain.planning_engine import PlanningEngine
from brain.critic import AdversarialCritic
from brain.failure_analyzer import FailureAnalyzer
from safety.sandbox import ExecutionSandbox
from evolution.evaluator import SystemEvaluator

class MasterOrchestrator:
    def __init__(self):
        print("\n⚡ [SWARM COGNITIVE MATRIX] Initializing Subsystems...")
        self.intent_engine = IntentEngine()
        self.planner = PlanningEngine()
        self.critic = AdversarialCritic()
        self.failure_analyzer = FailureAnalyzer()
        self.sandbox = ExecutionSandbox()
        self.evaluator = SystemEvaluator()
        self.task_queue = []
        
        self.business = BusinessAgent()
        self.coder = CoderAgent()
        self.reviewer = ReviewerAgent()
        self.memory = MemoryCore()

    def assign_task(self, agent_id, task):
        """Register a task for the swarm cycle without changing agent execution flow."""
        if not agent_id or not task:
            raise ValueError("agent_id and task are required")

        task_record = {
            "agent_id": str(agent_id),
            "task": str(task),
            "status": "queued"
        }
        self.task_queue.append(task_record)
        print(f"📋 [Task Router] Queued task for {task_record['agent_id']}: {task_record['task']}")
        return task_record

    async def run_full_swarm_cycle(self, user_input):
        # 0. Strict Input Validation
        clean_prompt = validate_and_clean_input(user_input)
        if not clean_prompt:
            print("⚠️ [Input Gate] Invalid or UI prompt echo detected. Aborting mission.")
            return

        intent_info = self.intent_engine.classify_intent(clean_prompt)
        print(f"\n🧭 [Intent Classifier] Input Type Detected: '{intent_info['intent']}'")

        if intent_info["intent"] == "RUN_COMMAND":
            print(f"⚙️ [System Exec Routing] Executing shell command: '{clean_prompt}'")
            os.system(clean_prompt)
            return

        business_niche = clean_prompt
        filename = generate_tool_name(business_niche)
        print(f"\n=================== 🚀 COGNITIVE MATRIX RUN: {business_niche[:50]}... ===================")
        print(f"📌 Clean Tool Slug: {filename}")

        # 1. Dynamic Planning & Strategy
        plan = self.planner.decompose_mission(business_niche)
        try:
            biz_plan = self.business.generate_monetization_plan(business_niche)
        except Exception as e:
            print(f"⚠️ Strategy warning: {e}")

        # 2. Solver Synthesis & Sandbox Evaluation Loop (With Auto-Repair)
        failure_context = None
        for repair_cycle in range(1, 3):
            print(f"\n🔄 --- Synthesis & Test Pass (Cycle {repair_cycle}) ---")
            created_file = self.coder.build_tool(business_niche, f"Automated engine for {business_niche}", failure_context)
            
            if not created_file or not os.path.exists(created_file):
                print("❌ File synthesis failed completely.")
                break

            with open(created_file, 'r') as f:
                code = f.read()

            critic_res = self.critic.critique_candidate(business_niche, code)
            sec_res = self.reviewer.review_code(code)
            sandbox_res = self.sandbox.Execute_and_benchmark(created_file)
            eval_res = self.evaluator.evaluate_build(sandbox_res, critic_res, sec_res)

            if eval_res["status"] == "PASS":
                print(f"\n✅ Mission Passed Empirical Gate on Cycle {repair_cycle}!")
                print(f"📊 Score: {eval_res['total_score']}/100 | Execution Latency: {sandbox_res['execution_time_ms']:.2f}ms")
                self.memory.save_learning(
                    business_niche, 
                    "NO_ERROR", 
                    f"Score: {eval_res['total_score']}/100 | File: {created_file}"
                )
                return
            else:
                print(f"⚠️ Attempt {repair_cycle} failed (Exit Code: {sandbox_res['exit_code']}). Triggering Diagnostic Analyzer...")
                diag = self.failure_analyzer.analyze_failure(sandbox_res)
                failure_context = f"Error Type: {diag['error_type']}\nTraceback: {diag['traceback_summary']}"

        print("\n❌ Mission failed after max repair cycles. Rollback triggered.")
