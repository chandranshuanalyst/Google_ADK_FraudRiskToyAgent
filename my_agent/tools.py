#Tools
def fetch_transaction_data():
    return {
        "transaction_id": "TXN_88421",
        "amount": 42000,
        "currency": "INR",
        "merchant_country": "RU",
        "channel": "CNP",
        "hour_of_day": 2
    }


def fetch_customer_snapshot():
    return {
        "customer_id": "CUST_77",
        "account_age_months": 14,
        "avg_txn_amount_90d": 4800,
        "txn_velocity_24h": 6,
        "previous_fraud_count": 1,
        "kyc_risk_rating": "Medium"
    }


def fraud_model_proxy(txn, cust):
    score = 0

    if txn["amount"] > 5 * cust["avg_txn_amount_90d"]:
        score += 35
    if txn["merchant_country"] != "IN":
        score += 25
    if cust["txn_velocity_24h"] > 5:
        score += 20
    if txn["channel"] == "CNP":
        score += 10
    if cust["previous_fraud_count"] > 0:
        score += 10

    return {
        "fraud_score": score,
        "amount_ratio": txn["amount"] / cust["avg_txn_amount_90d"],
        "velocity_24h": cust["txn_velocity_24h"],
        "geo_risk_flag": txn["merchant_country"] != "IN",
        "channel_risk_flag": txn["channel"] == "CNP"
    }
