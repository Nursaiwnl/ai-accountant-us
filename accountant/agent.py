import pandas as pd
from .rules import DEDUCTIBLE_RULES, KEYWORDS
from .calculator import estimate_taxes
from .llm import ask_llm
from .memory import AgentMemory

memory = AgentMemory()

def classify(description: str):
    desc = description.lower()
    for category, words in KEYWORDS.items():
        if any(word in desc for word in words):
            return category
    return "other"

def explain_expense(row):
    system = "You are a US tax accountant assistant."
    user = f"""
    Explain why this expense is or is not deductible:
    Description: {row['description']}
    Category: {row['category']}
    Deductible rate: {row['deductible_rate']}
    """
    explanation = ask_llm(system, user)
    memory.add(explanation)
    return explanation

def run_accountant(csv_file):
    df = pd.read_csv(csv_file)

    df["category"] = df["description"].apply(classify)
    df["deductible_rate"] = df["category"].map(
        lambda c: DEDUCTIBLE_RULES.get(c, 0.0)
    )
    df["deductible_amount"] = df["amount"] * df["deductible_rate"]

    income = df[df["amount"] > 0]["amount"].sum()
    expenses = df[df["amount"] < 0]["deductible_amount"].abs().sum()
    net_income = income - expenses

    taxes = estimate_taxes(net_income)

    memory.add(f"Calculated net income: {net_income}")

    return {
        "income": income,
        "expenses": expenses,
        "net_income": net_income,
        "taxes": taxes,
        "table": df,
        "memory": memory,
    }

