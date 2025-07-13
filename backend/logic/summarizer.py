import os
from openai import OpenAI
from typing import Optional

# Create OpenAI client with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(text: str, max_words: int = 150) -> Optional[str]:
    """
    Generate a brief summary from a longer document.
    Limits output to roughly `max_words`.
    """
    if not text:
        print("⚠️ No text provided to summarize.")
        return None

    input_chunk = text.strip()
    if len(input_chunk) > 4000:
        input_chunk = input_chunk[:4000]

    print("Summarizing text of length:", len(input_chunk))
    print("Sample prompt:", input_chunk[:200])

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"Summarize the following text in no more than {max_words} words. Be concise and focus on the main ideas."
                },
                {
                    "role": "user",
                    "content": input_chunk
                }
            ],
            temperature=0.4,
            max_tokens=300
        )
        summary = response.choices[0].message.content.strip()
        print("✅ Summary generated.")
        return summary
    except Exception as e:
        print("OpenAI API Error:", e)
        return None
