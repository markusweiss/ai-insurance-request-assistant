from fastapi import FastAPI, HTTPException

from app.schemas import RequestAnalysisInput, RequestAnalysisOutput
from app.services.analyzer import MistralAnalyzer


# Initializes the FastAPI application.
app = FastAPI(
    title="AI Insurance Request Assistant",
    description="Portfolio prototype for the pre-qualification of fictional insurance service requests.",
    version="0.1.0",
)


# Provides a health check endpoint to verify API availability.
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# Analyzes an incoming customer request using the AI service.
@app.post("/api/v1/requests/analyze", response_model=RequestAnalysisOutput)
def analyze_request(payload: RequestAnalysisInput) -> RequestAnalysisOutput:
    try:
        # Run the request analysis and prepare the API response.
        result = MistralAnalyzer().analyze(payload)
        return RequestAnalysisOutput(analysis=result)

    except Exception as exc:
        # Return a gateway error if the AI service fails.
        # In production, log a correlation ID and sanitized error details.
        raise HTTPException(
            status_code=502,
            detail="The request could not currently be analyzed by the AI service.",
        ) from exc
