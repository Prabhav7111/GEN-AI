from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from backend.utils.doc_parser import extract_text_from_pdf, extract_text_from_txt
from backend.logic.summarizer import summarize_text
from pydantic import BaseModel
from backend.logic.qa_engine import prepare_vector_index, answer_question
from backend.logic.question_gen import generate_questions, evaluate_answer

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
    return {"summary": summary or " Sorry, could not generate summary."}

class QuestionPayload(BaseModel):
    document: str
    query: str

@app.post("/ask/")
async def ask_question(payload: QuestionPayload):
    """
    Accepts full document + user question.
    Returns an answer with justification using vector-based retrieval.
    """
    if not payload.document.strip() or not payload.query.strip():
        return {"error": "Missing document text or question."}

    index = prepare_vector_index(payload.document)
    if not index:
        return {"error": "Could not process the document."}

    answer = answer_question(payload.query, index)
    return {"answer": answer or "No answer could be generated."}

class DocumentPayload(BaseModel):
    document: str

@app.post("/challenge/")
async def get_challenge_questions(payload: DocumentPayload):
    """
    Returns 3 logic-based questions from the uploaded document.
    """
    if not payload.document.strip():
        return {"error": "Missing document content."}

    questions = generate_questions(payload.document)
    return {"questions": questions or []}


class EvaluationPayload(BaseModel):
    document: str
    question: str
    user_answer: str

@app.post("/evaluate/")
async def evaluate_user_response(payload: EvaluationPayload):
    """
    Evaluates a user answer for a given question, based on the source document.
    """
    if not all([payload.document.strip(), payload.question.strip(), payload.user_answer.strip()]):
        return {"error": "Missing one or more required fields."}

    feedback = evaluate_answer(payload.document, payload.question, payload.user_answer)
    return {"feedback": feedback or "Could not evaluate answer."}


