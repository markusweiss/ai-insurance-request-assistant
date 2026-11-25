from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class Urgency(str, Enum):
    LOW = "niedrig"
    NORMAL = "normal"
    HIGH = "hoch"


class RequestAnalysisInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    subject: str | None = Field(default=None, max_length=300)
    message: str = Field(min_length=10, max_length=12000)


class ExtractedInformation(BaseModel):
    policy_number: str | None = None
    requested_start_date: str | None = None
    product_or_policy_type: str | None = None
    other_details: list[str] = Field(default_factory=list)


class RequestAnalysis(BaseModel):
    category: str = Field(description="Fachliche Kategorie, im MVP normalerweise Vertragsservice")
    customer_concern: str
    urgency: Urgency
    extracted_information: ExtractedInformation
    missing_information: list[str]
    summary: str
    recommended_next_step: str
    requires_human_review: bool = True
    limitations_note: str = (
        "Es wurde kein tatsächlicher Vertragsstatus geprüft. "
        "Die Analyse muss von einer zuständigen Person geprüft werden."
    )


class RequestAnalysisOutput(BaseModel):
    analysis: RequestAnalysis
