Agent ID

D4 – Blame Language Avoided

Purpose

To evaluate whether the learning response avoids blame-oriented language, including implicit or explicit attribution of fault to individuals or groups, in line with the LRRIT dimension “Blame language is avoided”.

Scope

This agent assesses only:

the presence or absence of blame-oriented language

how responsibility, causation, or error is framed linguistically

whether individuals are portrayed as at fault rather than as actors within a system

It does not:

assess whether errors occurred

judge correctness of clinical decisions

evaluate systems thinking (handled by D2)

infer blame unless linguistically present

Inputs

EvidencePack

narrative text chunks

table evidence (if language in tables is relevant, e.g. action logs)

LRRIT D4 rubric criteria (Good / Some / Little evidence)

Outputs

Rating: one of {GOOD, SOME, LITTLE}

Rationale: short explanation grounded in language evidence

Evidence citations:

text chunk IDs

table IDs (if relevant)

Uncertainty flag (optional)

Evaluation Logic (Non-algorithmic)

This agent performs interpretive linguistic assessment, not sentiment analysis.

Good evidence may include:

Clear avoidance of individualised blame

Use of neutral, systems-oriented phrasing

Explicit rejection of blame (e.g. “this was not due to individual error”)

Some evidence may include:

Mostly neutral language with isolated problematic phrases

Mixed framing (systems language plus occasional attribution to individuals)

Little evidence may include:

Explicit blame (e.g. “X failed to…”, “staff did not follow…”)

Repeated focus on individual behaviour without context

Moralising or judgemental language

Important distinctions

Describing an action ≠ assigning blame

Identifying error ≠ blaming

Naming roles ≠ attributing fault

The agent must focus on how things are described, not what happened.

Constraints

Do not infer blame from outcomes alone

Do not rely on keyword spotting without context

Do not penalise reports that name actions neutrally

Do not use document-level metadata or human judgements

Failure Modes

Borderline language (e.g. “did not”, “failed to”) that may or may not be blame-oriented

Very short reports with minimal language

Tables that list actions without narrative context

In these cases, the agent should:

explain ambiguity explicitly

set the uncertainty flag where appropriate

Interaction with LaJ

This agent’s output is evaluated by the LLM-as-Judge (LaJ) for:

rubric fidelity

evidence grounding

over- or under-interpretation of language