import os
from openai import OpenAI

# Берём ключ из переменных окружения
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_llm(system_prompt: str, user_prompt: str) -> str:
    """
    Вызывает LLM для анализа и объяснений.
    Если ключ не активен или лимит превышен, возвращает заглушку.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"LLM temporarily unavailable: {str(e)}"
