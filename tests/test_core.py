from pigeon_archive_agentbench.core import PigeonArchiveOrchestrator, ResearchPlannerAgent, EventExtractionAgent
from pigeon_archive_agentbench.corpus import DOCUMENTS

def test_planner_extracts_date():
    assert "1918" in ResearchPlannerAgent().plan("pigeon service in 1918")["dates"]

def test_retrieval_and_verification_has_provenance():
    result = PigeonArchiveOrchestrator().verify("British forces used carrier pigeons to send messages from front-line units")
    assert result["evidence"]
    assert result["provenance_audit"]["all_items_have_source_url"]

def test_event_extraction_is_traceable():
    events = EventExtractionAgent().extract(DOCUMENTS)
    assert events
    assert all(e["source_url"].startswith("https://") for e in events)

def test_unknown_claim_abstains():
    result = PigeonArchiveOrchestrator().verify("Pigeons operated nuclear submarines on Mars")
    assert result["verdict"]["label"] == "insufficient_evidence"
