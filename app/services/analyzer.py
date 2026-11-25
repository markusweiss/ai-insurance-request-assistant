from mistralai.client import Mistral

from app.config import settings
from app.prompts import SYSTEM_PROMPT
from app.schemas import RequestAnalysis, RequestAnalysisInput


# Analyzes incoming customer requests using the Mistral AI API.
class MistralAnalyzer:

    # Initializes the Mistral API client.
    def __init__(self) -> None:
        if not settings.mistral_api_key:
            raise RuntimeError("MISTRAL_API_KEY fehlt. Bitte .env konfigurieren.")

        self.client = Mistral(api_key=settings.mistral_api_key)

    # Analyzes a customer request and returns a structured result.
    def analyze(self, request: RequestAnalysisInput) -> RequestAnalysis:

        # Prepare the input for the AI model.
        user_content = (
            f"Subject: {request.subject or '(not provided)'}\n"
            f"Customer message:\n{request.message}"
        )

        # Send the request to Mistral and enforce the expected response schema.
        response = self.client.chat.parse(
            model=settings.mistral_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            response_format=RequestAnalysis,
        )

        # Extract the structured response.
        parsed = response.choices[0].message.parsed

        if parsed is None:
            raise RuntimeError("Mistral returned no structured analysis.")

        # Convert the response into a dictionary.
        data = parsed.model_dump()

        # Require human review for every analysis.
        data["requires_human_review"] = True

        # Validate and return the final analysis.
        return RequestAnalysis.model_validate(data)
