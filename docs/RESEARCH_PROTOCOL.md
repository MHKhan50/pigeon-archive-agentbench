# Research protocol

## Research questions
RQ1: How accurately can agentic NLP extract structured historical communication events from archive descriptions?
RQ2: Does provenance auditing reduce unsupported historical claims?
RQ3: How does multi-agent orchestration compare with TF-IDF-only retrieval?

## Annotation schema
Each gold event should contain: source_id, date (or unknown), force/service, location (or unknown), communication_role, event_outcome, evidence_span, and confidence.
Do not infer missing fields. Use `unknown` rather than guessing.

## Evaluation
- Event extraction: entity-level precision, recall, and F1.
- Claim verification: macro-F1, abstention coverage-risk, evidence precision/recall.
- Provenance: valid-source rate and evidence-span attribution accuracy.
- Agent efficiency: tool calls, latency, and tokens if a language model is added.

## v0.2 neural NLP extension
Add a compact transformer encoder for semantic retrieval or a token-classification model for event slots. Compare it with the CPU TF-IDF baseline on a manually annotated dataset. Keep archival source IDs and evidence spans attached to every prediction.

## Limitations
The included corpus is a small seed set of source-linked summaries, not a representative training corpus. Rule-assisted event extraction is a baseline, not a trained neural model. Historical anecdotes may be contested; triangulate before asserting.
