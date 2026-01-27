Agent ID

D2 – Systems Approach to Contributory Factors

Purpose

Assess whether the learning response adopts a systems approach—i.e., it considers contributory factors beyond individual actions, including processes, environment, communication pathways, resources, workflow, policy, escalation mechanisms, and organisational context.

Scope

This agent evaluates the framing and analysis of causes and improvements, not clinical correctness.

In scope

References to system/process contributors (handover, escalation, pathway design, workload, staffing, tooling, coordination)

Use of language indicating multi-factor causation

Improvement actions aimed at system-level changes (standardisation, redesign, checklists, training embedded in process, escalation protocols)

Out of scope

Accuracy of clinical conclusions

Blame language per se (handled by D4)

Compassionate engagement (D1)

Risk rating classification (post-processing agent)

Inputs

EvidencePack:

Text chunks

Table evidence (action logs, timelines, pathway checklists, etc.)

LRRIT D2 rubric criteria

Outputs

JSON object containing:

Rating: GOOD | SOME | LITTLE

Rationale

Evidence list (1–3 items) with:

id (Text/Table reference)

verbatim quote (≤25 words)

evidence_type (positive|negative)

uncertainty flag

Judgement criteria
GOOD evidence

Explicit systems framing: multiple contributory factors, interactions, barriers

Improvement actions target system redesign (pathway/escalation/process ownership)

Avoids individual-centric root causes as the primary explanation

SOME evidence

Mix of systems and individual framing

Systems factors mentioned but not integrated or not linked to actions

Actions partly system-level, partly individual reminders/training without structural change

LITTLE evidence

Primarily individual-centric framing (“clinician should have…”) with minimal process analysis

Improvement actions mainly admonitions, reminders, “be more vigilant”

Little recognition of organisational/structural contributors

Evidence polarity

positive: explicit system/process framing, multi-factor explanation, system-level interventions

negative: primarily individual-level causes/remedies, simplistic “human error” framing, or lack of systems analysis where expected

Constraints

Do not infer systems analysis if it is not stated

Do not treat “something went wrong” as systems thinking unless factors are articulated

Prefer exact quotes that show systems concepts (escalation pathway, handover, governance, capacity, process)

Failure modes

Confusing “system delay” narrative with systems analysis (needs explicit framing)

Over-crediting generic statements (“process issue”) without detail

Penalising necessary individual accountability statements where balanced systems analysis exists

Interaction with LaJ

LaJ should assess:

Rubric fidelity (does rating match evidence polarity?)

Quote validity (verbatim, properly sourced)

Over/under-interpretation of “systems language”