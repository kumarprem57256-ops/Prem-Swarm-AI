# PREM SWARM AI — Phase 2 Integration

## What this package adds

A provider-neutral autonomous development layer:

1. `CodebaseIntelligence` — read-only project map + relevant source context.
2. `ModelAdapter` — OpenAI-compatible HTTP adapter using environment variables.
3. `AutonomousArchitect` — structured JSON implementation plans.
4. `VerificationEngine` — compile/test gates.
5. `RepairEngine` — structured minimal repair proposals.
6. `IntegrationGate` — backups and protected paths.

## Important

This is an integration package, not a replacement for the current project.
Merge it into the current `~/Prem-Swarm-AI` tree. Do not restore the old backup over
the current tree because the current tree contains newer #1–#3 work.

## Environment variables

Do NOT put API keys in source:

`PREM_LLM_PROVIDER`
`PREM_LLM_ENDPOINT`
`PREM_LLM_MODEL`
`PREM_LLM_API_KEY`

The adapter expects an OpenAI-compatible chat-completions style response.

## Integration order

ModelAdapter → CodebaseIntelligence → Architect → Safe Patch/Backup
→ Verification → Repair → Verification → Integration Gate → Memory.

The existing `orchestrator.py`, Coder, Executor, Healer, Reviewer, Sandbox and
Memory components should remain the authoritative existing subsystems where their
interfaces are compatible.

No component is marked GREEN merely because code generation succeeded; verification
must pass first.
