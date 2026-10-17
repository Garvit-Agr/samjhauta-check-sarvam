from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class RedFlag(BaseModel):
    clause_quote: str = Field(
        ...,
        description="Verbatim or near-verbatim quote of the predatory/asymmetric clause from the contract.",
    )
    plain_english_risk: str = Field(
        ...,
        description="Brutally honest, clear breakdown of how this clause harms the user financially or legally.",
    )
    severity_level: Literal["Critical", "High", "Medium"] = Field(
        ...,
        description="Severity level of the trap: Critical (severe financial/legal peril), High (heavy unfair disadvantage), Medium (irritant/unfair friction).",
    )
    counter_proposal_text: str = Field(
        ...,
        description="Specific amended clause wording the user should propose as a replacement.",
    )


class AuditReport(BaseModel):
    document_type: str = Field(
        ...,
        description="Classification of document (e.g. Bangalore Residential Rental Agreement, Unsecured Personal Loan, Freelance NDA, Hospital Discharge Estimate).",
    )
    fairness_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Overall fairness score from 0 (heavily predatory/one-sided) to 100 (balanced and mutual).",
    )
    summary: str = Field(
        ...,
        description="High-level forensic executive summary of the document and risk profile.",
    )
    key_takeaways: List[str] = Field(
        default_factory=list,
        description="Quick punchy bullet points of primary hazards and negotiating leverage points.",
    )
    red_flags: List[RedFlag] = Field(
        default_factory=list,
        description="List of predatory, asymmetric, or dangerous clauses detected in the document.",
    )
    missing_protections: List[str] = Field(
        default_factory=list,
        description="Crucial standard protections, rights, or dispute mechanisms that the contract failed to include.",
    )
    whatsapp_negotiation_draft: str = Field(
        ...,
        description="A polite, culturally tactful, and firm message ready to copy-paste into WhatsApp/Email to initiate clause renegotiation.",
    )
    spoken_briefing_script: str = Field(
        ...,
        description="A colloquial, punchy 45-second audio briefing script explaining the traps in direct spoken style (as a protective 'Big Brother').",
    )


class AnalysisResponse(BaseModel):
    success: bool = True
    cached: bool = False
    document_hash: str
    filename: str
    report: AuditReport
    spoken_language: str
    audio_base64: Optional[str] = None
    translated_script: Optional[str] = None
    is_demo: bool = False
    notes: Optional[str] = None
