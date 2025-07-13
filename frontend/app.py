import streamlit as st
import requests

st.set_page_config(page_title="GEN-AI Assistant", layout="centered")
st.title("GEN-AI: Document Assistant")

uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

doc_text = ""
summary = ""

if uploaded_file:
    with st.spinner("Generating summary, hold on please", icon="🧠"):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        try:
            res = requests.post("http://localhost:8000/summarize/", files=files)
            result = res.json()
            summary = result.get("summary", "")
        except Exception:
            st.error("Error while summarizing the document.")

    if summary:
        st.subheader("📌 Summary")
        st.write(summary)

    # this is for extracting raw text from file (again) , to be used for Q&A
    try:
        file_bytes = uploaded_file.getvalue()
        if uploaded_file.name.endswith(".pdf"):
            from backend.utils.doc_parser import extract_text_from_pdf
            doc_text = extract_text_from_pdf(file_bytes)
        else:
            from backend.utils.doc_parser import extract_text_from_txt
            doc_text = extract_text_from_txt(file_bytes)
    except Exception:
        st.warning("Couldn't extract full text for Q&A.")

# here is implemented Ask Anything Mode
if doc_text:
    st.markdown("---")
    st.subheader("🤔 Ask Anything")

    user_question = st.text_input("Ask a question based on the document:")
    if user_question:
        with st.spinner("Thinking..."):
            try:
                payload = {
                    "document": doc_text,
                    "query": user_question
                }
                res = requests.post("http://localhost:8000/ask/", json=payload)
                result = res.json()
                answer = result.get("answer", "")

                st.markdown("**Answer:**")
                st.write(answer if answer else "No answer generated.")
            except Exception:
                st.error("Failed to get an answer from the backend.")
