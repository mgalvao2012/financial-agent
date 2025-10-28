from pydantic import BaseModel, Field
from typing import List, Literal

class FinancialSituation(BaseModel):
    """Financial health assessment"""
    overall_health: Literal["excellent", "good", "fair", "poor"]
    spending_pattern: str = Field(description="Description of spending behavior")
    savings_rate: float = Field(description="Estimated monthly savings rate")
    risk_indicators: List[str] = Field(description="Financial risk factors")
    opportunities: List[str] = Field(description="Financial improvement opportunities")

class LifeMoment(BaseModel):
    """Life moment identification"""
    detected_moments: List[str] = Field(description="Identified life events or transitions")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Confidence in detection")
    time_sensitivity: Literal["immediate", "near-term", "medium-term", "long-term"]
    relevant_needs: List[str] = Field(description="Needs arising from life moments")

class ChannelPreference(BaseModel):
    """Communication channel analysis"""
    primary_channel: Literal["email", "sms", "push_notification", "phone", "in_app"]
    secondary_channels: List[str]
    best_contact_time: str
    engagement_likelihood: float = Field(ge=0.0, le=1.0)
    personalization_level: Literal["high", "medium", "low"]

class NextBestAction(BaseModel):
    """Recommended action or offer"""
    action_type: Literal["product_offer", "service_upgrade", "financial_advice", "engagement"]
    specific_recommendation: str
    priority: Literal["high", "medium", "low"]
    expected_value: float = Field(description="Expected customer lifetime value impact")
    rationale: str

class HyperpersonalizedMessage(BaseModel):
    """Final synthesized output"""
    message_subject: str
    message_body: str
    call_to_action: str
    tone: Literal["professional", "friendly", "urgent", "educational"]
    personalization_elements: List[str]
    recommended_channel: str
    optimal_send_time: str
    expected_engagement_rate: float
