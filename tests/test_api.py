from fastapi.testclient import TestClient
import app.main as main


class FakeAnalyzer:
    def analyze(self, payload):
        from app.schemas import RequestAnalysis, Urgency
        return RequestAnalysis(
            category="Vertragsservice",
            customer_concern="Fehlende Vertragsunterlagen",
            urgency=Urgency.NORMAL,
            extracted_information={"policy_number": None},
            missing_information=["Vertragsnummer"],
            summary="Der Kunde hat noch keine Vertragsunterlagen erhalten.",
            recommended_next_step="Geeignete Identifikationsangaben erfragen und den Vorgang prüfen.",
            requires_human_review=True,
        )


def test_analyze_endpoint_returns_structured_result(monkeypatch):
    monkeypatch.setattr(main, "MistralAnalyzer", FakeAnalyzer)
    client = TestClient(main.app)

    response = client.post(
        "/api/v1/requests/analyze",
        json={
            "subject": "Fehlende Unterlagen",
            "message": "Ich habe meine Vertragsunterlagen noch nicht erhalten.",
        },
    )

    assert response.status_code == 200
    body = response.json()["analysis"]
    assert body["category"] == "Vertragsservice"
    assert body["requires_human_review"] is True
