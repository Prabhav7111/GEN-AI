import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_text(text: str, max_words: int = 150) -> str:
    if not text.strip():
        return None

    prompt = f"""
Summarize the following document into approximately {max_words} words. Be concise, capture main points clearly.

Document:
\"\"\"
{text[:8000]}
\"\"\"
Summary:
""".strip()

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("❌ Gemini Error:", e)
        return None
