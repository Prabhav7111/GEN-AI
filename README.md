# GEN-AI: Smart Document Assistant

A local GenAI powered assistant that processes user uploaded documents to:

- Generate a brief summary (≤150 words)
- Answer free form, context based questions
- Pose logic driven questions to test user understanding
- Provide clear justifications grounded in the document content

---

## Features

- **Ask Anything** — Users can query the document freely
- **Challenge Me** — System generates 3 reasoning based questions and evaluates user responses
- **Auto Summary** — Concise summary shown after upload
- **Answer Justification** — Each response cites its source within the document

---

## Supported File Types

- PDF (.pdf)
- Plain text (.txt)

---

## 🔐 Setup

1. Create a .env file in the project root  
2. Add your OpenAI key like: OPEN_API_KEY=sk.....
3. install requirements
4. run backend: uvicorn backend.main:app-- reload
5. run frontend: streamlit run frontend/app.py
