# backend/aml_ai.py

"""
نموذج مبسط لـ AML AI:
- يحسب درجة مخاطرة بناءً على الدولة والمبلغ.
- يرجع flag + level + score.
"""

HIGH_RISK_COUNTRIES = {"IR", "KP", "SY", "CU"}  # مثال دول عالية المخاطر

def _base_score(country: str, amount: float) -> float:
    score = 0.0
    if country in HIGH_RISK_COUNTRIES:
        score += 0.7
    if amount > 10000:
        score += 0.3
    elif amount > 5000:
        score += 0.2
    elif amount > 1000:
        score += 0.1
    return score

async def aml_ai_check(user_id: str, country: str, amount: float):
    score = _base_score(country, amount)

    if score >= 0.8:
        level = "HIGH"
        flag = True
    elif score >= 0.4:
        level = "MEDIUM"
        flag = True
    else:
        level = "LOW"
        flag = False

    return {
        "user_id": user_id,
        "country": country,
        "amount": amount,
        "score": score,
        "level": level,
        "flag": flag
    }
