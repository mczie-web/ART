# McZie Adoption Plan for ART (v1)

## Objective
Adopt ART (Agent Reinforcement Trainer) in McZie to improve reliability of multi-step agent workflows with measurable business outcomes.

## Phase 1 (2 weeks) — Controlled Pilot
Use case: **Sales next-action quality and prioritization**.

### Scope
- Input: active opportunities from Sala de Máquinas (pipeline CSV/API).
- Agent output:
  1. next best action (verb-first, owner, due date),
  2. risk score (0-100),
  3. close-likelihood band.
- Human-in-the-loop approval required before outbound execution.

### Reward design (initial)
- +1: action accepted by sales lead.
- +1: action executed on time.
- +2: opportunity advances stage within SLA window.
- -1: action rejected as low-quality.
- -2: no action field / invalid owner / invalid due date.

### Success criteria
- >=25% reduction in opportunities without clear next action.
- >=20% reduction in overdue follow-ups.
- >=10pp improvement in stage progression rate for at-risk opportunities.

## Phase 2 (2–4 weeks) — Production Hardening
- Versioned reward functions.
- Weekly offline eval set with fixed benchmark tasks.
- Safety rules for legal/commercial red lines.
- Observability (cost, latency, reward trend, drift).

## Integration architecture (target)
1. McZie Sala de Máquinas exports normalized opportunity trajectories.
2. ART training loop runs per batch window.
3. Best checkpoint promoted to inference endpoint.
4. Dashboard consumes model recommendations + confidence.

## Guardrails
- Never auto-send client messages without human approval in pilot.
- Block recommendations on missing critical fields (owner, date, stage).
- Log every recommendation + final human decision for audit.

## Immediate next tasks
1. Build trajectory schema for sales opportunities.
2. Create 100-sample eval set from historical pipeline events.
3. Implement baseline reward function module.
4. Run first local/hosted ART training cycle.
5. Compare baseline vs trained policy in offline eval.
