"""Validation utilities for PigeonArchive-AgentBench historical event annotations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set

from pigeon_archive_agentbench.corpus import DOCUMENTS


COMMUNICATION_ROLES = {
    "message_delivery",
    "message_receipt",
    "messenger_service",
    "emergency_communication",
    "other",
    "unknown",
}

DATE_STATUSES = {
    "explicit",
    "partial",
    "unknown",
    "ambiguous",
}

CONFIDENCE_LEVELS = {"high", "medium", "low"}
ANNOTATION_STATUSES = {"independent", "adjudicated"}

REQUIRED_FIELDS = {
    "event_id",
    "source_id",
    "evidence_text",
    "evidence_start",
    "evidence_end",
    "date",
    "date_status",
    "force_service",
    "location",
    "communication_role",
    "event_action",
    "event_outcome",
    "confidence",
    "uncertainty_note",
    "annotator_id",
    "annotation_status",
}

OPTIONAL_FIELDS = {"annotation_guide_version"}


def validate_annotation(
    record: Dict[str, Any],
    source_texts: Optional[Dict[str, str]] = None,
) -> List[str]:
    """Return validation errors for one annotation record."""
    errors: List[str] = []

    if not isinstance(record, dict):
        return ["Annotation must be a JSON object."]

    missing = REQUIRED_FIELDS - set(record)
    unexpected = set(record) - REQUIRED_FIELDS - OPTIONAL_FIELDS

    if missing:
        errors.append("Missing required fields: " + ", ".join(sorted(missing)))

    if unexpected:
        errors.append("Unexpected fields: " + ", ".join(sorted(unexpected)))

    if missing:
        return errors

    for field in ("event_id", "source_id", "annotator_id"):
        value = record[field]
        if not isinstance(value, str) or not value.strip():
            errors.append("{} must be a non-empty string.".format(field))

    if not isinstance(record["evidence_text"], str) or not record["evidence_text"]:
        errors.append("evidence_text must be a non-empty string.")

    for field in ("evidence_start", "evidence_end"):
        value = record[field]
        if isinstance(value, bool) or not isinstance(value, int):
            errors.append("{} must be an integer.".format(field))

    if (
        isinstance(record["evidence_start"], int)
        and not isinstance(record["evidence_start"], bool)
        and isinstance(record["evidence_end"], int)
        and not isinstance(record["evidence_end"], bool)
    ):
        start = record["evidence_start"]
        end = record["evidence_end"]
        if start < 0:
            errors.append("evidence_start cannot be negative.")
        if end <= start:
            errors.append("evidence_end must be greater than evidence_start.")

        if isinstance(record["evidence_text"], str) and end > start:
            if end - start != len(record["evidence_text"]):
                errors.append(
                    "Evidence offsets do not match the evidence_text length."
                )

            source_id = record["source_id"]
            source = (
                (source_texts or {}).get(source_id)
                if isinstance(source_id, str)
                else None
            )
            if source is not None:
                if end > len(source):
                    errors.append("Evidence span exceeds the source text length.")
                elif source[start:end] != record["evidence_text"]:
                    errors.append(
                        "evidence_text does not match the source text at the "
                        "specified offsets."
                    )

    date_value = record["date"]
    if date_value is not None and (
        not isinstance(date_value, str) or not date_value.strip()
    ):
        errors.append("date must be a non-empty string or null.")

    date_status = record["date_status"]
    if not isinstance(date_status, str) or date_status not in DATE_STATUSES:
        errors.append("date_status must be one of: " + ", ".join(sorted(DATE_STATUSES)))

    if date_status == "unknown" and date_value is not None:
        errors.append("date must be null when date_status is 'unknown'.")

    for field in ("force_service", "location", "event_action", "event_outcome"):
        value = record[field]
        if value is not None and (
            not isinstance(value, str) or not value.strip()
        ):
            errors.append("{} must be a non-empty string or null.".format(field))

    communication_role = record["communication_role"]
    if (
        not isinstance(communication_role, str)
        or communication_role not in COMMUNICATION_ROLES
    ):
        errors.append(
            "communication_role must be one of: "
            + ", ".join(sorted(COMMUNICATION_ROLES))
        )

    confidence = record["confidence"]
    if not isinstance(confidence, str) or confidence not in CONFIDENCE_LEVELS:
        errors.append(
            "confidence must be one of: " + ", ".join(sorted(CONFIDENCE_LEVELS))
        )

    annotation_status = record["annotation_status"]
    if (
        not isinstance(annotation_status, str)
        or annotation_status not in ANNOTATION_STATUSES
    ):
        errors.append(
            "annotation_status must be one of: "
            + ", ".join(sorted(ANNOTATION_STATUSES))
        )

    note = record["uncertainty_note"]
    if note is not None and not isinstance(note, str):
        errors.append("uncertainty_note must be a string or null.")

    if "annotation_guide_version" in record:
        version = record["annotation_guide_version"]
        if not isinstance(version, str) or not version.strip():
            errors.append("annotation_guide_version must be a non-empty string.")

    if source_texts is not None:
        source_id = record["source_id"]
        if not isinstance(source_id, str) or source_id not in source_texts:
            errors.append("source_id does not exist in the supplied corpus.")

    return errors


def load_jsonl(
    path: str,
    source_texts: Optional[Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    """Load JSONL annotations, rejecting malformed or invalid records."""
    records: List[Dict[str, Any]] = []
    seen_event_ids: Set[str] = set()
    file_path = Path(path)

    with file_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    "Invalid JSON on line {}: {}".format(line_number, exc)
                ) from exc

            errors = validate_annotation(record, source_texts)
            if errors:
                raise ValueError(
                    "Invalid annotation on line {}: {}".format(
                        line_number, "; ".join(errors)
                    )
                )

            event_id = record["event_id"]
            if event_id in seen_event_ids:
                raise ValueError(
                    "Duplicate event_id {!r} on line {}.".format(
                        event_id, line_number
                    )
                )

            seen_event_ids.add(event_id)
            records.append(record)

    return records


def corpus_source_texts() -> Dict[str, str]:
    """Return the researcher-written seed texts keyed by corpus source ID."""
    return {document["id"]: document["text"] for document in DOCUMENTS}


def validate_jsonl(path: str) -> List[Dict[str, Any]]:
    """Validate and load a JSONL file against the current seed corpus."""
    return load_jsonl(path, source_texts=corpus_source_texts())
