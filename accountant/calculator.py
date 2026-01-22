def estimate_taxes(net_income: float) -> dict:
    self_employment_tax = net_income * 0.153
    income_tax = net_income * 0.10

    return {
        "self_employment_tax": round(self_employment_tax, 2),
        "income_tax": round(income_tax, 2),
        "total_tax": round(self_employment_tax + income_tax, 2),
    }
