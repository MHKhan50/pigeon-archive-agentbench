import json

from pigeon_archive_agentbench.cli import main
from pigeon_archive_agentbench.annotation import corpus_source_texts


def valid_record():
    source_id = "awm-pigeons-war"
    source = corpus_source_texts()[source_id]
    evidence = "During the First World War"
    start = source.index(evidence)

    return {
        "event_id": "event-cli-001",
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


def test_cli_accepts_empty_annotation_file(tmp_path, monkeypatch, capsys):
    path = tmp_path / "empty.jsonl"
    path.write_text("", encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv", ["pigeonbench", "validate-annotations", str(path)]
    )

    assert main() == 0
    output = json.loads(capsys.readouterr().out)
    assert output["valid"] is True
    assert output["records"] == 0


def test_cli_accepts_valid_annotation(tmp_path, monkeypatch, capsys):
    path = tmp_path / "valid.jsonl"
    path.write_text(json.dumps(valid_record()) + "\n", encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv", ["pigeonbench", "validate-annotations", str(path)]
    )

    assert main() == 0
    output = json.loads(capsys.readouterr().out)
    assert output["valid"] is True
    assert output["records"] == 1


def test_cli_rejects_invalid_annotation(tmp_path, monkeypatch, capsys):
    record = valid_record()
    record["communication_role"] = "invalid_role"
    path = tmp_path / "invalid.jsonl"
    path.write_text(json.dumps(record) + "\n", encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv", ["pigeonbench", "validate-annotations", str(path)]
    )

    assert main() == 1
    output = capsys.readouterr()
    assert "Annotation validation failed" in output.err


def test_cli_reports_missing_annotation_file(tmp_path, monkeypatch, capsys):
    path = tmp_path / "missing.jsonl"
    monkeypatch.setattr(
        "sys.argv", ["pigeonbench", "validate-annotations", str(path)]
    )

    assert main() == 1
    output = capsys.readouterr()
    assert "Annotation validation failed" in output.err
