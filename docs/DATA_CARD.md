# Data Card

## Dataset overview

The seed corpus contains six short, researcher-written summaries of public-facing pages from museums, archives, and national institutions. Each record stores a source title, institution, URL, and summary. Original source text, archival scans, and photographs are not redistributed.

## Intended use

The corpus supports software smoke tests, early-stage retrieval experiments, provenance demonstrations, and development of annotation tooling. It is not currently suitable for claims of broad historical coverage, representative sampling, or reliable generalisation.

## Composition and limitations

The corpus is intentionally small and was not assembled through a systematic archival sampling procedure. It is not a balanced dataset, an expert-annotated gold standard, or a comprehensive record of wartime carrier-pigeon use. Researcher-written summaries may omit context and should not be treated as substitutes for primary-source evidence.

## Annotation status

The pilot annotation file is currently empty. No independent expert annotations, adjudicated gold labels, or inter-annotator agreement results are claimed. The annotation schema and validation procedure are documented in `data/annotations/README.md` and `docs/RESEARCH_PROTOCOL.md`.

## Source provenance and rights

Each seed record identifies its originating institution and source URL. Public accessibility does not establish permission to reproduce or redistribute source material. Item-level rights and applicable institutional policies require review before reuse or dataset redistribution. See `docs/SOURCE_LICENSING_REGISTER.md`.

## Expansion requirements

A future research dataset requires systematic archival sampling, documented inclusion and exclusion criteria, source-level rights review, independent annotation by qualified annotators, adjudication, and a reproducible evaluation split. Any expanded release should preserve provenance and document uncertainty, missing information, and known coverage gaps.
