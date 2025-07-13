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

def evaluate_answer(document_text: str, question: str, user_answer: str) -> Optional[str]:
    """
    Evaluates a user answers to a question using the document for reference.
    Returns a feedback string with justification.
    """
    prompt = f"""
You're evaluating an answer based on a source document.
Read the document and question below.
Then evaluate user answers, using only the document to justify your feedback.

Document:
\"\"\"
{document_text[:3000]}
\"\"\"

Question: {question}

User's Answer: {user_answer}

Give constructive feedback, say if it's correct, partially right, or wrong, and explain briefly why.
""".strip()

    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=300
        )
        return res['choices'][0]['message']['content'].strip()
    except Exception:
        return None


