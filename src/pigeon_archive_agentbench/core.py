import re
from typing import Dict, Any, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .corpus import DOCUMENTS

class ResearchPlannerAgent:
    name = "research_planner"
    def plan(self, query: str) -> Dict[str, Any]:
        dates = re.findall(r"\b(?:18|19|20)\d{2}\b", query)
        terms = [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z-]{2,}", query)
                 if w.lower() not in {"the", "and", "for", "with", "were", "was"}]
        return {"query_terms": terms[:15], "dates": dates,
                "retrieval_plan": "search curated archive summaries; retain source provenance"}

class ArchiveRetrievalAgent:
    name = "archive_retrieval"
    def retrieve(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        docs = [d["text"] for d in DOCUMENTS]
        matrix = TfidfVectorizer(stop_words="english", ngram_range=(1, 2)).fit_transform([query] + docs)
        scores = cosine_similarity(matrix[0:1], matrix[1:]).ravel()
        ranked = sorted(zip(scores, DOCUMENTS), key=lambda x: x[0], reverse=True)[:top_k]
        return [{"id": d["id"], "title": d["title"], "source": d["source"],
                 "url": d["url"], "text": d["text"], "score": float(score)}
                for score, d in ranked if score > 0]

class EventExtractionAgent:
    name = "event_extractor"
    def extract(self, docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        events = []
        for doc in docs:
            text = doc["text"]
            year = re.search(r"\b(?:18|19|20)\d{2}\b", text)
            roles = []
            for phrase in ["front-line", "mobile lofts", "aircraft", "home base", "message capsules", "Second World War"]:
                if phrase.lower() in text.lower():
                    roles.append(phrase)
            if any(k in text.lower() for k in ["used", "carried", "messages", "service"]):
                events.append({"event_type": "wartime_communication",
                               "date_mentioned": year.group(0) if year else None,
                               "roles_or_context": roles,
                               "source_id": doc["id"], "source_url": doc["url"],
                               "extraction_method": "transparent rule-assisted NLP"})
        return events

class ClaimVerifierAgent:
    name = "claim_verifier"
    def verify(self, query: str, evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
        score = max((e["score"] for e in evidence), default=0.0)
        return {"label": "supported" if score >= 0.18 else "insufficient_evidence",
                "similarity_score": round(score, 4),
                "method": "TF-IDF lexical retrieval threshold; not a historical truth probability",
                "caveat": "A high lexical score identifies relevant passages, not proof of truth."}

class ProvenanceAuditorAgent:
    name = "provenance_auditor"
    def audit(self, evidence, events):
        all_items = evidence + events
        return {"items_checked": len(all_items),
                "all_items_have_source_url": all(bool(x.get("url") or x.get("source_url")) for x in all_items)}

class PigeonArchiveOrchestrator:
    def __init__(self):
        self.planner = ResearchPlannerAgent()
        self.retriever = ArchiveRetrievalAgent()
        self.extractor = EventExtractionAgent()
        self.verifier = ClaimVerifierAgent()
        self.auditor = ProvenanceAuditorAgent()

    def verify(self, claim: str) -> Dict[str, Any]:
        plan = self.planner.plan(claim)
        evidence = self.retriever.retrieve(claim)
        verdict = self.verifier.verify(claim, evidence)
        events = self.extractor.extract(evidence)
        audit = self.auditor.audit(evidence, events)
        return {"project": "PigeonArchive-AgentBench", "version": "0.1.0", "claim": claim,
                "plan": plan, "verdict": verdict, "evidence": evidence,
                "events": events, "provenance_audit": audit,
                "agent_trace": [self.planner.name, self.retriever.name, self.extractor.name,
                                self.verifier.name, self.auditor.name],
                "research_only": True}

    def extract_all(self):
        events = self.extractor.extract(DOCUMENTS)
        return {"project": "PigeonArchive-AgentBench", "events": events,
                "provenance_audit": self.auditor.audit([], events)}
