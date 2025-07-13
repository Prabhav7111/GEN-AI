import os
import openai
from typing import Optional

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_text(text: str, max_words: int = 150) -> Optional[str]:
    """
    generate a brief summary from a longer document.
    and limit output to roughly `max_words`.
    """
    if not text:
        return None

    input_chunk = text.strip()
    if len(input_chunk) > 4000:
        input_chunk = input_chunk[:4000]  # trim excessive input so keep it simple

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Summarize the following text in no more than 150 words. Be concise and stick to the core ideas."
                },
                {
                    "role": "user",
                    "content": input_chunk
                }
            ],
            temperature=0.4,
            max_tokens=300
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception:
        return None

