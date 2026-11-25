import json

import pytest

from pigeon_archive_agentbench.annotation import (
    corpus_source_texts,
    load_jsonl,
    validate_annotation,
)


def valid_record():
    source_id = "awm-pigeons-war"
    source = corpus_source_texts()[source_id]
    evidence = "During the First World War"
    start = source.index(evidence)

    return {
        "event_id": "event-001",
        "source_id": source_id,
        "evidence_text": evidence,
        "evidence_start": start,
        "evidence_end": start + len(evidence),
        "date": "1914-1918",
        "date_status": "partial",
        "force_service": "British Expeditionary Force",
        "location": None,
        "communication_role": "message_delivery",
        "event_action": "used carrier pigeons",
        "event_outcome": None,
        "confidence": "high",
        "uncertainty_note": None,
        "annotator_id": "annotator-01",
        "annotation_status": "independent",
        "annotation_guide_version": "0.2.0",
    }


def test_valid_annotation_passes():
    record = valid_record()
    assert validate_annotation(record, corpus_source_texts()) == []


def test_evidence_must_match_source_offsets():
    record = valid_record()
    record["evidence_text"] = "Incorrect evidence"

    errors = validate_annotation(record, corpus_source_texts())
    assert any("length" in error for error in errors)


def test_unknown_source_is_rejected():
    record = valid_record()
    record["source_id"] = "missing-source"

    errors = validate_annotation(record, corpus_source_texts())
    assert any("does not exist" in error for error in errors)


def test_invalid_communication_role_is_rejected():
    record = valid_record()
    record["communication_role"] = "military_activity"

    errors = validate_annotation(record, corpus_source_texts())
    assert any("communication_role" in error for error in errors)


def test_unknown_date_must_be_null():
    record = valid_record()
    record["date_status"] = "unknown"
    record["date"] = "1918"

    errors = validate_annotation(record, corpus_source_texts())
    assert any("date must be null" in error for error in errors)


def test_boolean_offsets_are_rejected():
    record = valid_record()
    record["evidence_start"] = True

    errors = validate_annotation(record, corpus_source_texts())
    assert any("evidence_start must be an integer" in error for error in errors)


def test_jsonl_loader_rejects_duplicate_event_ids(tmp_path):
    record = valid_record()
    path = tmp_path / "annotations.jsonl"
    path.write_text(
        json.dumps(record) + "\n" + json.dumps(record) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Duplicate event_id"):
        load_jsonl(str(path), corpus_source_texts())


def test_jsonl_loader_rejects_malformed_json(tmp_path):
    path = tmp_path / "malformed.jsonl"
    path.write_text('{"event_id": invalid}\n', encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON"):
        load_jsonl(str(path), corpus_source_texts())


def load_annotation_schema():
    from pathlib import Path

    schema_path = (
        Path(__file__).resolve().parents[1]
        / "src"
        / "pigeon_archive_agentbench"
        / "schemas"
        / "annotation.schema.json"
    )
    return json.loads(schema_path.read_text(encoding="utf-8"))


def test_annotation_schema_is_valid_draft_2020_12():
    from jsonschema import Draft202012Validator

    schema = load_annotation_schema()
    Draft202012Validator.check_schema(schema)


def test_valid_record_passes_json_schema():
    from jsonschema import Draft202012Validator

    schema = load_annotation_schema()
    validator = Draft202012Validator(schema)

    errors = list(validator.iter_errors(valid_record()))
    assert errors == []


def test_schema_rejects_missing_required_field():
    from jsonschema import Draft202012Validator

    record = valid_record()
    del record["event_id"]

    validator = Draft202012Validator(load_annotation_schema())
    errors = list(validator.iter_errors(record))

    assert any("event_id" in error.message for error in errors)


def test_schema_rejects_invalid_communication_role():
    from jsonschema import Draft202012Validator

    record = valid_record()
    record["communication_role"] = "military_activity"

    validator = Draft202012Validator(load_annotation_schema())
    errors = list(validator.iter_errors(record))

    assert any(
        error.path and error.path[-1] == "communication_role"
        for error in errors
    )


def test_schema_rejects_undefined_properties():
    from jsonschema import Draft202012Validator

    record = valid_record()
    record["unapproved_field"] = "unexpected"

    validator = Draft202012Validator(load_annotation_schema())
    errors = list(validator.iter_errors(record))

    assert any("Additional properties" in error.message for error in errors)


def test_schema_rejects_negative_evidence_offsets():
    from jsonschema import Draft202012Validator

    record = valid_record()
    record["evidence_start"] = -1

    validator = Draft202012Validator(load_annotation_schema())
    errors = list(validator.iter_errors(record))

    assert any(
        error.path and error.path[-1] == "evidence_start"
        for error in errors
    )



@pytest.mark.parametrize(
    ("field", "value", "expected"),
    [
        ("source_id", ["awm-pigeons-war"], "source_id must be"),
        ("date_status", ["partial"], "date_status must be"),
        ("communication_role", ["message_delivery"], "communication_role"),
        ("confidence", ["high"], "confidence must be"),
        ("annotation_status", ["independent"], "annotation_status must be"),
    ],
)
def test_unhashable_field_values_return_validation_errors(field, value, expected):
    record = valid_record()
    record[field] = value

    errors = validate_annotation(record, corpus_source_texts())

    assert any(expected in error for error in errors)
