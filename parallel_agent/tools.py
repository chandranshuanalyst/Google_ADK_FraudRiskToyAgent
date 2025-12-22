def get_transaction_data() -> dict:
    return {
        "amount": 4200,
        "avg_customer_amount": 1200,
        "merchant_category": "Electronics",
        "merchant_risk_score": 0.75,  # proxy
        "hour_of_day": 22
    }

def score_transaction_risk(txn: dict) -> float:
    score = 0.0

    if txn["amount"] > 3 * txn["avg_customer_amount"]:
        score += 0.4

    if txn["merchant_risk_score"] > 0.7:
        score += 0.3

    if txn["hour_of_day"] >= 22:
        score += 0.2

    return min(score, 1.0)

def get_behavior_data() -> dict:
    return {
        "txn_velocity_1h": 4,
        "spend_deviation": 2.8,
        "prior_fraud": True,
        "account_tenure_years": 1.2
    }
def score_behavior_risk(behavior: dict) -> float:
    score = 0.0

    if behavior["txn_velocity_1h"] >= 4:
        score += 0.4

    if behavior["spend_deviation"] >= 2.5:
        score += 0.3

    if behavior["prior_fraud"]:
        score += 0.2

    return min(score, 1.0)
def get_country_data() -> dict:
    return {
        "transaction_country": "IN",
        "home_country": "IN",
        "is_high_risk_country": False,
        "recent_country_changes": 2
    }
def score_country_risk(country: dict) -> float:
    score = 0.0

    if country["is_high_risk_country"]:
        score += 0.5

    if country["recent_country_changes"] >= 2:
        score += 0.3

    return min(score, 1.0)
