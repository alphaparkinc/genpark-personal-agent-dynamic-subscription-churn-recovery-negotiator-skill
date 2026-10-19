# -*- coding: utf-8 -*-
"""Dynamic Subscription Churn & Retention Bargaining Skill for GenPark Personal Agents."""
import json
from typing import Dict, Any

def simulate_retention_flow_concession(service_name: str, current_monthly_fee_usd: float, subscription_age_months: int, competitor_alternative_fee_usd: float = 0.0) -> Dict[str, Any]:
    cumulative_spend_usd = round(current_monthly_fee_usd * subscription_age_months, 2)
    
    # Loyalty factor
    if subscription_age_months >= 24:
        churn_risk_budget_pct = 40.0
        retention_likelihood = "VERY_HIGH (Tier-1 Loyal Customer)"
    elif subscription_age_months >= 12:
        churn_risk_budget_pct = 30.0
        retention_likelihood = "HIGH (Established User)"
    else:
        churn_risk_budget_pct = 20.0
        retention_likelihood = "MODERATE (Standard Concession Threshold)"

    target_concession_fee_usd = round(current_monthly_fee_usd * (1.0 - (churn_risk_budget_pct / 100.0)), 2)
    annual_savings_usd = round((current_monthly_fee_usd - target_concession_fee_usd) * 12, 2)

    return {
        "service": service_name,
        "current_monthly_fee_usd": current_monthly_fee_usd,
        "tenure_months": subscription_age_months,
        "cumulative_paid_usd": cumulative_spend_usd,
        "predicted_retention_offer_discount_pct": churn_risk_budget_pct,
        "target_negotiated_fee_usd": target_concession_fee_usd,
        "projected_annual_savings_usd": annual_savings_usd,
        "retention_concession_probability": retention_likelihood,
        "competitor_price_spread_usd": round(current_monthly_fee_usd - competitor_alternative_fee_usd, 2) if competitor_alternative_fee_usd > 0 else 0.0,
        "tactical_guidance": "Initiate cancellation flow up to the confirmation dialog to trigger automated retention modal."
    }

def generate_cancellation_negotiation_script(service_name: str, primary_reason: str, desired_discount_pct: float) -> Dict[str, Any]:
    if primary_reason == "too_expensive":
        argument = (
            f"I have thoroughly enjoyed using {service_name}, but recent budget restructuring forces me to trim discretionary software expenses. "
            f"If {service_name} can extend an ongoing loyalty rate with {desired_discount_pct:.0f}% off, I would gladly stay subscribed."
        )
    elif primary_reason == "switching_to_competitor":
        argument = (
            f"I am preparing to migrate to an alternative market provider that offers comparable core workflows at a more competitive price point. "
            f"Matching that value with a {desired_discount_pct:.0f}% rate concession would avert my migration."
        )
    else:
        argument = (
            f"My workflow has shifted temporarily, making full-price subscription unjustifiable. "
            f"A pause tier or a temporary {desired_discount_pct:.0f}% discount over the next 6 months would allow me to maintain my workspace."
        )

    return {
        "service": service_name,
        "reason_category": primary_reason,
        "concierge_negotiation_pitch": argument,
        "support_chat_ready_text": f"Agentic Retention Inquiry: {argument}",
        "negotiator": "GenPark Consumer Finance Advocate"
    }
