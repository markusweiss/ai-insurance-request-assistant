from mistralai.client import Mistral

from app.config import settings
from app.prompts import SYSTEM_PROMPT
from app.schemas import RequestAnalysis, RequestAnalysisInput


class MistralAnalyzer:
    def __init__(self) -> None:
        if not settings.mistral_api_key:
            raise RuntimeError("MISTRAL_API_KEY fehlt. Bitte .env konfigurieren.")
        self.client = Mistral(api_key=settings.mistral_api_key)

    def analyze(self, request: RequestAnalysisInput) -> RequestAnalysis:
        user_content = (
            f"Betreff: {request.subject or '(nicht angegeben)'}\n"
            f"Kundennachricht:\n{request.message}"
        )

        response = self.client.chat.parse(
            model=settings.mistral_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            response_format=RequestAnalysis,
        )

        parsed = response.choices[0].message.parsed
        if parsed is None:
            raise RuntimeError("Mistral hat keine strukturierte Analyse zurückgegeben.")

        data = parsed.model_dump()
        data["requires_human_review"] = True
        return RequestAnalysis.model_validate(data)
