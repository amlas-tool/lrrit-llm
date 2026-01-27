Agent ID

D1 – Compassionate Engagement

Purpose

To evaluate whether the learning response demonstrates compassionate engagement with people affected by the incident, including patients, families, staff, or others, in line with the LRRIT dimension “People affected are involved and considered”.

Scope

This agent assesses only:

how people affected are described, acknowledged, or involved

whether perspectives, experiences, or impacts are represented

whether the tone reflects compassion, respect, and dignity

It does not:

assess correctness of facts

judge clinical quality

infer intent beyond what is stated

assess other LRRIT dimensions (e.g. blame, systems, actions)

Inputs

EvidencePack

narrative text chunks

table evidence (if relevant, e.g. feedback tables)

LRRIT D1 rubric criteria (Good / Some / Little evidence)

Outputs

Rating: one of {GOOD, SOME, LITTLE}

Rationale: short explanation grounded in evidence

Evidence citations:

text chunk IDs (page + chunk)

table IDs + page numbers (if used)

Uncertainty flag (optional):

set when evidence is sparse or ambiguous

Evaluation Logic (Non-algorithmic)

The agent applies interpretive judgement, not checklist scoring.

Indicators include (non-exhaustive):

Good evidence may include:

Explicit reference to experiences or perspectives of affected people

Evidence that staff or patients were listened to or involved

Language indicating empathy, dignity, or care

Acknowledgement of emotional, moral, or practical impacts

Some evidence may include:

Acknowledgement that people were affected, without depth

Generic or indirect references (e.g. “staff concerns were noted”)

Limited representation of perspectives

Little evidence may include:

No mention of people affected

Purely technical or procedural narrative

Dehumanised or impersonal descriptions

Constraints

Do not infer compassion from outcomes alone

Do not assume involvement unless stated

Do not penalise brevity if evidence is genuinely limited

Do not use metadata or document-level features (these are for LaJ only)

Failure Modes (to be tolerated, not hidden)

Ambiguous evidence

Very short reports

Reports where compassion may have occurred but is undocumented

In such cases, the agent should:

rate conservatively

explicitly state uncertainty

Interaction with LaJ

This agent does not self-evaluate.

Its output is passed unchanged to:

the LLM-as-Judge (LaJ) for reasoning-quality evaluation

later human comparison