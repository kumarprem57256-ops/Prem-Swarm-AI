import sys
import json
import time
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.progress import SpinnerColumn, Progress, TextColumn
from rich.syntax import Syntax
from rich.table import Table

from orchestrator import MasterOrchestrator
from agent_researcher import ResearcherAgent
from agent_media import MediaAgent
from agent_coder import CoderAgent
from agent_executor import CodeExecutorAgent

console = Console()

def display_banner():
    banner_text = Text("PREM SWARM AI: AUTONOMOUS 4-AGENT DASHBOARD", style="bold cyan")
    console.print(Panel(banner_text, border_style="cyan", expand=False))

def start_swarm():
    console.clear()
    display_banner()

    try:
        user_topic = console.input("\n[bold yellow]Enter Swarm Mission Topic[/bold yellow] (or 'exit' to quit): ").strip()
    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red][EXITING] Swarm Shutdown.[/bold red]")
        sys.exit(0)

    if not user_topic or user_topic.lower() == 'exit':
        console.print("\n[bold red][EXITING] No mission provided.[/bold red]")
        sys.exit(0)

    console.print(f"\n[bold green]🚀 MISSION INITIALIZED:[/bold green] [bold white]'{user_topic}'[/bold white]\n")

    master = MasterOrchestrator()
    researcher = ResearcherAgent()
    media_worker = MediaAgent()
    coder_worker = CoderAgent()
    executor_worker = CodeExecutorAgent()

    # --- STEP 1: RESEARCH ---
    with Progress(SpinnerColumn("dots", style="bold magenta"), TextColumn("[bold magenta]{task.description}"), transient=True) as progress:
        progress.add_task(description="[Agent 02] Conducting Deep Technical Research...", total=None)
        master.assign_task(researcher.agent_id, f"Research insights for '{user_topic}'")
        research_res = researcher.research_topic(user_topic)
        research_context = research_res.get("research_data", "")
        master.log_completion(researcher.agent_id, f"Research insights for '{user_topic}'", research_context)

    console.print("✅ [bold magenta]Agent 02 (Researcher):[/bold magenta] Technical Insights Captured")

    # --- STEP 2: MEDIA STRATEGY ---
    with Progress(SpinnerColumn("dots", style="bold yellow"), TextColumn("[bold yellow]{task.description}"), transient=True) as progress:
        progress.add_task(description="[Agent 01] Formulating Viral Media Strategy...", total=None)
        media_prompt = f"{user_topic}\n\nResearch Insights:\n{research_context}"
        master.assign_task(media_worker.agent_id, "Generate viral strategy")
        media_res = media_worker.process_trend_task(media_prompt)
        media_output = media_res.get("ai_output", "")
        master.log_completion(media_worker.agent_id, "Generate viral strategy", media_output)

    console.print("✅ [bold yellow]Agent 01 (Media):[/bold yellow] High-Engagement Strategy Generated")

    # --- STEP 3: CODE MVP ---
    with Progress(SpinnerColumn("dots", style="bold cyan"), TextColumn("[bold cyan]{task.description}"), transient=True) as progress:
        progress.add_task(description="[Agent 03] Building Clean Code/MVP Architecture...", total=None)
        master.assign_task(coder_worker.agent_id, "Build code prototype")
        coder_res = coder_worker.generate_code(media_output)
        master.log_completion(coder_worker.agent_id, "Build code prototype", json.dumps(coder_res))

    console.print("✅ [bold cyan]Agent 03 (Coder):[/bold cyan] Python MVP Script Built")

    # --- STEP 4: EXECUTION & SELF-HEALING ---
    with Progress(SpinnerColumn("dots", style="bold green"), TextColumn("[bold green]{task.description}"), transient=True) as progress:
        progress.add_task(description="[Agent 04] Executing Python Script Live...", total=None)
        master.assign_task(executor_worker.agent_id, "Execute generated python MVP")
        exec_res = executor_worker.execute_python_code(coder_res)

    max_retries = 2
    retry_count = 0

    while exec_res.get("status") == "Error" and retry_count < max_retries:
        retry_count += 1
        error_msg = exec_res.get("output", "")
        console.print(f"\n[bold red]⚠️  SELF-HEALING TRIGGERED (Attempt {retry_count}/{max_retries})[/bold red]")
        console.print(f"[dim red]Error: {error_msg}[/dim red]")

        fix_prompt = f"Previous code failed with error:\n{error_msg}\nRewrite the code using standard Python built-ins without uninstalled external libraries."
        with Progress(SpinnerColumn("dots", style="bold red"), TextColumn("[bold red]Self-Healing Code Fix in Progress..."), transient=True) as progress:
            progress.add_task(description="Fixing Code...", total=None)
            coder_res = coder_worker.generate_code(fix_prompt)
            exec_res = executor_worker.execute_python_code(coder_res)

    master.log_completion(executor_worker.agent_id, "Execute generated python MVP", json.dumps(exec_res))
    console.print("✅ [bold green]Agent 04 (Executor):[/bold green] Live Execution Finished")

    # --- DASHBOARD SUMMARY OUTPUT ---
    console.print("\n")
    
    # Strategy Panel
    console.print(Panel(media_output, title="[bold yellow]🔥 AGENT 01: VIRAL MEDIA STRATEGY[/bold yellow]", border_style="yellow"))

    # Live Execution Output Panel
    exec_status = exec_res.get("status")
    status_color = "bold green" if exec_status == "Success" else "bold red"
    
    exec_body = f"Status: [{status_color}]{exec_status}[/{status_color}]\n\nTerminal Stdout:\n{exec_res.get('output')}"
    console.print(Panel(exec_body, title="[bold green]⚡ AGENT 04: LIVE TERMINAL EXECUTION[/bold green]", border_style="green"))

if __name__ == "__main__":
    start_swarm()
