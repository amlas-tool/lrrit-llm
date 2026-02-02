# LaJ — LLM-as-Judge meta-evaluation layer (agent output QA)

## Purpose
Evaluate the quality of each dimension agent’s output (D1–D8) as a rubric-faithful evaluator.
LaJ judges the agent’s reasoning process and evidence use, not the underlying report.

## Inputs
- The dimension agent JSON output:
  - rating, rationale, evidence[] (id, quote, evidence_type), uncertainty
- A *limited* evidence context:
  - only the text blocks referenced by evidence ids (not the whole report)
- Dimension descriptor:
  - the LRRIT dimension name + short definition (what the agent is supposed to judge)

## Output
Structured metric basket scores and an overall judgement:
- per-metric score (PASS / WARN / FAIL)
- concise notes (actionable)
- overall (PASS / WARN / FAIL)
- flags for:
  - missing evidence, poor grounding, rubric mismatch, hallucination risk, etc.

## Metric basket (recommended default)
1. Rubric Fidelity
   - Does the rationale address the intended LRRIT judgement criteria for the dimension?
2. Evidence Grounding
   - Are claims in the rationale supported by the cited excerpts?
3. Reasoning Quality & Internal Coherence
   - Does the rationale logically support the rating without generic/circular statements?
4. Values Alignment (PSIRF/LRRIT)
   - Does the rationale reflect PSIRF/LRRIT values (systems thinking, compassion, local rationality, avoid blame/counterfactual misuse)?
5. Transparency & Uncertainty Handling
   - Is uncertainty signalled appropriately for mixed/ambiguous evidence?
6. Hallucination Screening (agent-output level)
   - Does the rationale introduce claims not supported by the supplied excerpts?

## Notes on “Hallucination”
LaJ should not re-read the full report. It should:
- validate that quoted excerpts exist in referenced evidence blocks (programmatic)
- flag rationale claims that are unsupported by the provided excerpts
