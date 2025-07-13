import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_text(text: str, max_words: int = 150) -> str:
    if not text:
        print(" No input text provided.")
        return None

    input_chunk = text.strip()
    if len(input_chunk) > 4000:
        input_chunk = input_chunk[:4000]

    print("🧾 Prompt being sent to OpenAI:", input_chunk[:200], "...")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"Summarize the following text in no more than {max_words} words. Be concise and stick to core ideas."
                },
                {
                    "role": "user",
                    "content": input_chunk
                }
            ],
            temperature=0.4,
            max_tokens=300
        )
        summary = response['choices'][0]['message']['content'].strip()
        print("✅ Summary Generated:", summary[:100], "...")
        return summary
    except Exception as e:
        print("❌ OpenAI API Error:", e)
        return None
