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

def llm_categorize(df):
    """
    Используем LLM для анализа описаний и предложения категорий.
    Возвращает DataFrame с колонкой 'llm_category' и 'llm_explanation'.
    """
    llm_categories = []
    explanations = []

    system = "You are a US tax accountant assistant. Categorize these expenses and explain why."

    for _, row in df.iterrows():
        user_prompt = f"Expense description: {row['description']}\nAmount: {row['amount']}\nSuggest a category and explain."
        explanation = ask_llm(system, user_prompt)
        explanations.append(explanation)

        # Попробуем выделить категорию из текста LLM (если не найдёт — fallback)
        found = "other"
        for cat in KEYWORDS.keys():
            if cat.lower() in explanation.lower():
                found = cat
                break
        llm_categories.append(found)

    df["llm_category"] = llm_categories
    df["llm_explanation"] = explanations
    return df

def run_accountant(csv_file):
    df = pd.read_csv(csv_file)

    # Сначала LLM предобрабатывает
    df = llm_categorize(df)

    # Агент классифицирует (железные расчёты)
    df["category"] = df["description"].apply(classify)
    df["deductible_rate"] = df["category"].map(lambda c: DEDUCTIBLE_RULES.get(c, 0.0))
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
