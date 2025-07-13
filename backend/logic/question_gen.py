import os
import openai
from typing import List, Optional

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_questions(document_text: str, count: int = 3) -> List[str]:
    """
    asks GPT to generate x logic-based questions based on the document.
    """
    prompt = f"""
You're a tutor testing comprehension of a document.
Based strictly on the content below, write {count} reasoning-based or logic-checking questions.
Please avoid generic or surface-level ones — focus on things that require inference or understanding.

Document:
\"\"\"
{document_text[:3000]}
\"\"\"
Questions:
""".strip()

    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=500
        )
        output = res['choices'][0]['message']['content'].strip()
        questions = [q.strip("-•123. ").strip() for q in output.split("\n") if q.strip()]
        return questions[:count]
    except Exception:
        return []

