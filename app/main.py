from fastapi import FastAPI, HTTPException

from app.schemas import RequestAnalysisInput, RequestAnalysisOutput
from app.services.analyzer import MistralAnalyzer

app = FastAPI(
    title="AI Insurance Request Assistant",
    description="Portfolio-Prototyp zur Vorqualifizierung fiktiver Vertragsservice-Anfragen.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/requests/analyze", response_model=RequestAnalysisOutput)
def analyze_request(payload: RequestAnalysisInput) -> RequestAnalysisOutput:
    try:
        result = MistralAnalyzer().analyze(payload)
        return RequestAnalysisOutput(analysis=result)
    except Exception as exc:
        # In production, log a correlation ID and sanitized error details.
        raise HTTPException(
            status_code=502,
            detail="Die Anfrage konnte aktuell nicht durch den KI-Dienst analysiert werden.",
        ) from exc
