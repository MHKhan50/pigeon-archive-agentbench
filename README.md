# WarBird-AgentBench v0.1.0

A lightweight **Agentic NLP** research benchmark for extracting and verifying historical facts about military carrier pigeons, focusing on First and Second World War records.

## Research objective
Can a multi-agent NLP pipeline turn historical prose into traceable events (date, force, location, role, outcome) and verify a natural-language claim against source-linked evidence while abstaining when sources are insufficient?

This is historical-document analysis only. It is not a military operational tool.

## Why carrier pigeons?
Official museum, archive and historical collections preserve material on wartime pigeon services, mobile lofts, message capsules, and documented incidents. The project uses these records as a source-grounded NLP task rather than inventing operational datasets.

## Agent architecture
1. **Research planner**: identifies entities, dates, and likely evidence concepts.
2. **Archive retrieval agent**: searches a local curated source corpus (offline-first; no fabricated web scraping).
3. **Event extraction agent**: extracts candidate event attributes with transparent NLP patterns.
4. **Claim verifier**: ranks passages with TF-IDF and returns supported / insufficient evidence.
5. **Provenance auditor**: requires each extracted event to retain a source URL.
6. **Orchestrator**: produces JSON report and trace.

## Quick start (macOS)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest -q
warbird --help
warbird demo
warbird verify --claim "Carrier pigeons were used by British forces to send messages from front-line units."
warbird extract
```

## NLP methods
- TF-IDF retrieval with word bigrams
- rule-assisted named entity/date/event cue extraction
- multi-agent orchestration with inspectable tool trace
- conservative abstention if similarity is weak

This is an NLP research baseline, not a trained neural model. v0.2 should compare a compact transformer encoder (e.g. sentence-transformers) against TF-IDF on a manually annotated, source-grounded benchmark.

## Research integrity
The included corpus contains concise researcher-written summaries and source links, not copied full articles. Historical claims may be contested; the Smithsonian's Cher Ami fact sheet explicitly discusses evidentiary uncertainty. The system therefore stores provenance and should not treat popular stories as established fact without corroboration.

## Primary references
- Australian War Memorial, Pigeons in War: https://www.awm.gov.au/articles/encyclopedia/pigeons-in-war
- National Army Museum, The British Army entrusted its secrets to birdbrains: https://www.nam.ac.uk/explore/british-army-entrusted-its-secrets-birdbrains
- Library of Congress, Pigeons in War research guide: https://guides.loc.gov/chronicling-america-war-pigeons
- Scottish Archives for Schools, Carrier Pigeons: https://www.scottisharchivesforschools.org/firstWorldWar/CarrierPigeons.asp
- Smithsonian National Museum of American History, Cher Ami fact sheet: https://americanhistory.si.edu/press/fact-sheets/cher-ami-fact-sheet-century-myth-and-public-memory

## Suggested paper title
*WarBird: A Provenance-Aware Agentic NLP Benchmark for Extracting and Verifying Historical Military Carrier-Pigeon Events*
