from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from backend.utils.doc_parser import extract_text_from_pdf, extract_text_from_txt
from backend.logic.summarizer import summarize_text

app = FastAPI()

# used streamlit to connect frontend locally
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/summarize/")
async def summarize_document(file: UploadFile = File(...)):
    """
    receive a PDF or TXT file and returns a 150-word summary.
    """
    content = await file.read()
    text = ""

    if file.filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(content)
    elif file.filename.lower().endswith(".txt"):
        text = extract_text_from_txt(content)
    else:
        return {"error": "Unsupported file type. Only .pdf and .txt are allowed."}

    summary = summarize_text(text)
    return {"summary": summary or " Sorry could not generate summary."}
