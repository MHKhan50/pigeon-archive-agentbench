# WarBird-AgentBench

**Research branch:** `research/v0.2.0` | **Baseline:** `v0.1.0`

A provenance-aware Agentic NLP benchmark for extracting and verifying historical wartime carrier-pigeon events from the First and Second World Wars.

## Research objective

Can a multi-agent NLP pipeline extract structured historical communication events, retrieve source-linked evidence, and assess claims while preserving provenance and uncertainty?

This is historical-document analysis only, not a military operational tool.

## Agent architecture

1. **Research planner:** identifies query concepts, entities, and dates.
2. **Archive retrieval agent:** searches a curated local source corpus.
3. **Event extraction agent:** extracts candidate attributes using rule-assisted NLP.
4. **Claim verifier:** ranks passages using TF-IDF lexical retrieval.
5. **Provenance auditor:** checks source references for evidence and extracted events.
6. **Orchestrator:** coordinates agents and produces JSON output and an inspectable trace.

## Quick start

Python 3.9 or later:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pytest -q
warbird --help
warbird demo
```

## Main commands

```bash
warbird verify --claim "British forces used carrier pigeons during the First World War."
warbird extract
warbird validate-annotations data/annotations/pilot_annotations.jsonl
```

The annotation validator checks structure, field values, unique event IDs, source identifiers, and evidence spans. JSON Schema Draft 2020-12 adds structural validation. The pilot file is intentionally empty: zero invalid records does not establish an annotated dataset or gold standard.

## Methods and research status

The baseline uses TF-IDF retrieval, word-level features and bigrams, rule-assisted event/date extraction, multi-agent orchestration, source-linked evidence, and provenance checks. Lexical similarity is not a probability of historical truth and does not independently prove a claim.

Planned comparisons include lexical versus semantic/hybrid retrieval, agentic versus non-agentic workflows, abstention, and efficiency. These require an independently annotated evaluation dataset. No expert-annotated gold standard or completed empirical evaluation is currently claimed.

## Data limitations and research integrity

The corpus contains six researcher-written summaries linked to institutional sources. It is small, not systematically sampled, and neither balanced nor comprehensive. Summaries are not substitutes for primary-source evidence. The project does not redistribute full source articles, archival scans, or photographs; public accessibility does not automatically grant reuse rights.

## Research documentation

- `docs/RESEARCH_PROTOCOL.md` — research questions, annotation, and evaluation.
- `docs/DATA_CARD.md` — dataset composition, intended use, and limitations.
- `docs/SOURCE_LICENSING_REGISTER.md` — provenance and rights-review status.
- `data/annotations/README.md` — annotation format and validation.
- `REFERENCES.md` — institutional references.

## Institutional references

- Australian War Memorial: https://www.awm.gov.au/articles/encyclopedia/pigeons-in-war
- National Army Museum: https://www.nam.ac.uk/explore/british-army-entrusted-its-secrets-birdbrains
- Library of Congress: https://guides.loc.gov/chronicling-america-war-pigeons
- Scottish Archives for Schools: https://www.scottisharchivesforschools.org/firstWorldWar/CarrierPigeons.asp
- Smithsonian National Museum of American History: https://americanhistory.si.edu/press/fact-sheets/cher-ami-fact-sheet-century-myth-and-public-memory
- U.S. Naval History and Heritage Command: https://www.history.navy.mil/browse-by-topic/exploration-and-innovation/navy-pigeons.html

## Suggested paper title

*WarBird-AgentBench: A Provenance-Aware Agentic NLP Benchmark for Historical Wartime Communication Event Extraction and Evidence Verification*
