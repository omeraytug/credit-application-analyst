"""Structured credit memo schema for multi-agent report generation."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class SourceReference(BaseModel):
    """Grounding reference so analysts can verify figures and claims."""

    source_id: str = Field(..., description="Stable id, e.g. financials.json#revenue")
    label: str = Field(..., description="Human-readable source name")
    excerpt: str | None = Field(
        default=None,
        description="Short quote or value pulled from the source document",
    )


class CustomerMetadata(BaseModel):
    """Static customer facts from mock data (not LLM-invented contact details)."""

    customer_name: str = Field(..., description="Display name of the applicant")
    customer_slug: str = Field(
        ...,
        description="Folder key under data/customers/, e.g. acme_corp",
    )
    industry: str | None = None
    country: str | None = None
    employee_count: int | None = None
    years_in_operation: int | None = None


class FinancialAnalysis(BaseModel):
    """Output of the financial analyst agent."""

    summary: str = Field(..., description="Narrative financial assessment")
    revenue_trend: str | None = Field(
        default=None, description="e.g. growing, flat, declining"
    )
    profitability: str | None = None
    liquidity: str | None = None
    leverage: str | None = None
    key_metrics: dict[str, str] = Field(
        default_factory=dict,
        description="Named metrics with values as strings, e.g. {'debt_to_equity': '1.2'}",
    )
    strengths: list[str] = Field(default_factory=list)
    concerns: list[str] = Field(default_factory=list)
    sources: list[SourceReference] = Field(default_factory=list)


class BusinessAnalysis(BaseModel):
    """Output of the business analyst agent."""

    summary: str = Field(..., description="Narrative business assessment")
    company_overview: str | None = None
    market_position: str | None = None
    management_and_governance: str | None = None
    competitive_landscape: str | None = None
    strengths: list[str] = Field(default_factory=list)
    concerns: list[str] = Field(default_factory=list)
    sources: list[SourceReference] = Field(default_factory=list)


class RiskAssessment(BaseModel):
    """Output of the risk analyst agent."""

    summary: str = Field(..., description="Overall risk narrative")
    risk_rating: Literal["low", "medium", "high", "critical"] = Field(
        ...,
        description="Overall credit risk band",
    )
    key_risk_factors: list[str] = Field(default_factory=list)
    mitigants: list[str] = Field(default_factory=list)
    recommendation: Literal["approve", "approve_with_conditions", "decline", "refer"] = (
        Field(..., description="Credit recommendation for human review")
    )
    conditions: list[str] = Field(
        default_factory=list,
        description="Covenants or conditions if approve_with_conditions",
    )
    sources: list[SourceReference] = Field(default_factory=list)


class CreditReport(BaseModel):
    """Full structured credit memo produced by the orchestrator."""

    report_id: str = Field(..., description="Unique id for this generated report")
    case_id: str | None = Field(
        default=None,
        description="Workflow case id when tied to async processing",
    )
    customer: CustomerMetadata
    generated_at: datetime = Field(
        ...,
        description="UTC timestamp when the report was assembled",
    )
    executive_summary: str | None = Field(
        default=None,
        description="Optional top-level summary across all sections",
    )
    financial_analysis: FinancialAnalysis
    business_analysis: BusinessAnalysis
    risk_assessment: RiskAssessment

    model_config = {"json_schema_extra": {"title": "CreditReport"}}
