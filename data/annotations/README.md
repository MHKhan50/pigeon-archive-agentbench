# Annotation Data

This directory contains the annotation schema and pilot annotation file.

## Files

- `../../src/warbird_agentbench/schemas/annotation.schema.json`: JSON Schema Draft 2020-12.
- `pilot_annotations.jsonl`: Reserved for independently produced pilot annotations. It is intentionally empty.

## Annotation format

Each non-empty JSONL line contains one annotation object. Required fields are defined in `../../src/warbird_agentbench/schemas/annotation.schema.json`. The optional `annotation_guide_version` records the annotation guideline version.

Evidence offsets use Python string indexing: `evidence_start` is zero-based and inclusive; `evidence_end` is exclusive. The evidence text must match the source text at those offsets exactly.

The Python validator checks record structure, field values, unique event IDs, source IDs, and evidence against the current researcher-written seed corpus. JSON Schema provides a separate structural check.

## Validation

Run from the repository root:

    warbird validate-annotations data/annotations/pilot_annotations.jsonl

A successful validation of an empty file means only that zero invalid records were found. It does not establish an annotation dataset or gold standard.

## Research status

The pilot file is intentionally empty. No historical annotations are claimed as expert-validated ground truth. The six current source summaries are researcher-written seed material, not a substitute for independent annotation of archival evidence.

The research protocol requires independent annotation, documented adjudication, and appropriate inter-annotator agreement analysis before a gold-standard evaluation set can be claimed.

Do not label fabricated, model-generated, or unverified records as expert annotations. Preserve annotator provenance and uncertainty.
