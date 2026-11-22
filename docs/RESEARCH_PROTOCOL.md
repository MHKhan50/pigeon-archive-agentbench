# Research Protocol

**Project:** WarBird-AgentBench
**Protocol version:** 0.2.0
**Research status:** Proposed methodology; expert annotation and empirical evaluation are not yet complete.

## 1. Research questions

- **RQ1:** How accurately can agentic NLP extract structured historical communication events from archive descriptions?
- **RQ2:** Does provenance auditing reduce unsupported historical claims?
- **RQ3:** How does multi-agent orchestration compare with TF-IDF-only retrieval?
- **RQ4:** Does semantic or hybrid retrieval improve evidence retrieval over a lexical TF-IDF baseline?
- **RQ5:** How reliably can independent annotators identify event attributes and supporting evidence in historical source descriptions?

## 2. Scope and unit of analysis

The initial benchmark concerns historical carrier-pigeon communication, principally during the First and Second World Wars.

The annotation unit is a source-grounded event assertion: a statement describing an action, communication activity, service, or outcome associated with carrier pigeons.

A source document may contain:
- No eligible event.
- One eligible event.
- Multiple distinct events.
- General background information that cannot be assigned to a specific event.

Annotators must not manufacture event records from general background statements.

The current six-record corpus consists of researcher-written summaries linked to institutional pages. These summaries are not equivalent to original archival documents or complete source texts. Annotation claims must identify which material was actually reviewed.

## 3. Annotation schema

Each event record should contain the following fields:

| Field | Description | Permitted representation |
|---|---|---|
| `event_id` | Stable identifier for the annotated event | Unique string |
| `source_id` | Corpus source identifier | Existing corpus ID |
| `evidence_text` | Exact text supporting the event | Verbatim span from the reviewed material |
| `evidence_start` | Start character offset of the evidence span | Integer, zero-based |
| `evidence_end` | Exclusive end character offset | Integer |
| `date` | Explicit event date or date expression | ISO date, year, partial date, or null |
| `date_status` | Whether the date is stated or unavailable | `explicit`, `partial`, `unknown`, `ambiguous` |
| `force_service` | Military force, service, or organisation | Text span or `unknown` |
| `location` | Explicit geographical location | Text span or `unknown` |
| `communication_role` | Role of the pigeon communication activity | Controlled label below |
| `event_action` | Action explicitly described | Text span or `unknown` |
| `event_outcome` | Explicitly stated result | Text span or `unknown` |
| `confidence` | Annotator's confidence in the event interpretation | `high`, `medium`, `low` |
| `uncertainty_note` | Explanation of ambiguity or missing context | Text or null |
| `annotator_id` | Pseudonymous annotator identifier | Stable project-specific ID |
| `annotation_status` | Review status | `independent`, `adjudicated` |

### 3.1 Communication-role labels

Use one primary label:

- `message_delivery`: a pigeon is described as carrying a message.
- `message_receipt`: a message is explicitly described as received.
- `messenger_service`: a pigeon communication service or system is described without a specific delivery event.
- `emergency_communication`: communication is explicitly associated with an emergency or loss of other communication methods.
- `other`: an eligible communication role not represented above.
- `unknown`: the role cannot be established from the reviewed evidence.

Do not assign a specific role merely because a source mentions pigeons in a military context.

### 3.2 Missing information and uncertainty

Use the following distinctions:

- `unknown`: the reviewed material does not state the value.
- `ambiguous`: the material contains information, but more than one interpretation is plausible.
- `partial`: only part of a date or attribute is available.
- `not_applicable`: the field does not apply to this event.
- `null`: no value can be supplied without inference.

Do not treat `unknown`, `ambiguous`, and `not_applicable` as interchangeable.

Annotators must not infer dates, locations, identities, military units, outcomes, or causal relationships from general historical knowledge.

### 3.3 Evidence-span rules

1. Copy evidence spans exactly from the material presented to the annotator.
2. Preserve original spelling, punctuation, and capitalisation.
3. Use zero-based character offsets with an exclusive end offset.
4. Keep spans as short as possible while retaining enough context to support the label.
5. Each non-unknown event attribute must be traceable to an evidence span.
6. If the reviewed material is a researcher-written summary, record that fact in the annotation metadata.
7. Do not present a paraphrase as a verbatim evidence span.
8. If an event requires multiple non-contiguous passages, record separate evidence spans rather than inventing one continuous passage.

## 4. Annotator qualifications and independence

The proposed gold-standard process requires two independent annotators for each item.

At least one annotator should have relevant historical, archival, or military-history expertise. The second should have suitable historical research or annotation experience.

Before annotation begins:

1. Provide the annotation guide and a short training set.
2. Discuss the label definitions and edge cases.
3. Conduct a pilot annotation.
4. Revise unclear instructions before the main annotation round.
5. Freeze the annotation guide version for each formal round.

Independent annotators must not see each other's labels or decisions before submitting their own annotations.

Annotator qualifications, training, conflicts of interest, and project roles should be documented without publishing unnecessary personal information.

**Status:** No expert annotation completion is claimed by this protocol. Annotator recruitment, qualifications, and actual annotation remain to be documented.

## 5. Disagreement and adjudication

After independent annotation:

1. Compare event identification, attribute labels, and evidence spans.
2. Preserve both original annotation records.
3. Categorise disagreements, for example:
   - Event boundary disagreement.
   - Date or location disagreement.
   - Communication-role disagreement.
   - Evidence-span boundary disagreement.
   - Ambiguous or unsupported interpretation.
4. Refer unresolved disagreements to a designated adjudicator with relevant historical or archival expertise.
5. Record the adjudicated decision and a concise rationale.
6. Never overwrite the original independent annotations.

If evidence is insufficient, retain `unknown` or `ambiguous` rather than forcing agreement.

The adjudicated dataset must preserve annotator-level records so that agreement can be independently evaluated.

## 6. Inter-annotator agreement

Report agreement before adjudication.

Recommended measures:

- **Cohen's kappa:** categorical labels with two annotators, where its assumptions are appropriate.
- **Raw percentage agreement:** report alongside chance-corrected agreement.
- **Span-level precision, recall, and F1:** compare evidence spans using an explicitly documented exact-match or overlap-matching rule.
- **Attribute-level agreement:** report separately for date status, communication role, force/service, location, and event outcome.
- **Event identification agreement:** report matching rules and unmatched events.

For rare labels or highly imbalanced categories, explain the limitations of kappa and consider an additional prevalence-robust agreement statistic.

Report the number of items, class distributions, missing labels, and confidence intervals where feasible. Do not interpret a single agreement statistic as proof of annotation validity.

## 7. Evaluation methodology

### 7.1 Event extraction

- Entity- and attribute-level precision, recall, and F1.
- Event identification precision, recall, and F1.
- Evidence-span exact-match and overlap F1.
- Performance broken down by attribute and source.
- Error analysis for unknown, ambiguous, and partially specified attributes.

### 7.2 Retrieval

Compare:
- TF-IDF lexical retrieval baseline.
- Compact transformer semantic retrieval.
- Hybrid lexical and semantic retrieval, if implemented.

Report:
- Recall@K.
- Mean Reciprocal Rank (MRR).
- Evidence passage precision and recall.
- Results by query type and source.

Use fixed query sets, documented preprocessing, and reproducible random seeds where applicable.

### 7.3 Claim verification

Use three evidence-grounded labels:

- `supported`: retrieved evidence directly supports the claim.
- `contradicted`: retrieved evidence directly conflicts with the claim.
- `insufficient_evidence`: available evidence does not justify either conclusion.

Report macro-F1, per-class precision and recall, abstention coverage-risk, and evidence attribution accuracy.

A lexical similarity score is not a probability that a historical claim is true. Retrieval relevance alone must not determine a historical truth label.

### 7.4 Provenance

Evaluate:
- Source identifier validity.
- Source URL availability and traceability.
- Evidence-span attribution accuracy.
- Whether the cited material actually supports the associated claim.
- Whether third-party or archival material has been distinguished from institutional commentary.

A URL-presence check alone is not sufficient to establish provenance validity.

### 7.5 Agent efficiency

Where applicable, report:
- Number of agent/tool calls.
- Wall-clock latency.
- Token usage.
- Retrieval and inference costs.
- Abstention and error rates.

Compare systems under equivalent data, query, and computational conditions.

## 8. Experimental design and reproducibility

- Preserve the v0.1.0 baseline as a separate Git commit.
- Record software versions, configuration, random seeds, and dataset versions.
- Keep source identifiers attached to every retrieved passage and prediction.
- Prevent train/test leakage through duplicate or closely related source material.
- Where multiple records refer to the same underlying source or event, use grouped splits where appropriate.
- Report all exclusions and preprocessing decisions.
- Store experiment configurations and machine-readable outputs.
- Do not report unexecuted experiments or hypothetical results as findings.

## 9. Source rights and dataset governance

Consult `docs/SOURCE_LICENSING_REGISTER.md` before expanding or redistributing the corpus.

The current seed corpus contains researcher-written summaries linked to institutional pages. It is not a collection of unrestricted archival source texts.

Before releasing additional source material or annotations:

- Verify page-level and item-level reuse conditions.
- Distinguish institutional text from third-party archival material.
- Document contributor terms for expert annotations.
- Avoid redistribution of material without appropriate rights.
- Record source and annotation provenance.
- Review whether annotations themselves contain restricted copied material.

## 10. v0.2.0 implementation plan

1. Formalise the source and rights register.
2. Finalise annotation schema and guidelines.
3. Build a machine-readable annotation format and validation tests.
4. Create a pilot annotation workflow.
5. Recruit and document qualified independent annotators.
6. Conduct pilot annotation and revise ambiguous instructions.
7. Complete independent annotation and adjudication.
8. Evaluate TF-IDF and semantic retrieval on the resulting gold set.
9. Evaluate extraction, verification, provenance, and agent efficiency.
10. Publish reproducible results with explicit limitations.

These are planned activities, not completed research outcomes.

## 11. Limitations

The current six-record corpus is a small seed set of source-linked researcher-written summaries. It is not representative of the full historical record and is not yet an expert-annotated gold-standard dataset.

Rule-assisted event extraction and TF-IDF retrieval are baseline methods, not validated historical reasoning systems.

Historical anecdotes, including individual pigeon stories, may be contested or shaped by later commemoration. Claims should be triangulated against appropriate primary and secondary sources.

The system supports research discovery and evidence organisation. It does not establish historical truth automatically, replace expert historical judgement, or certify the authenticity of archival material.
