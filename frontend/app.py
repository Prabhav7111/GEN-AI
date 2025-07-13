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



# Challenge Me Mode
if doc_text:
    st.markdown("---")
    st.subheader("🧠 Challenge Me")

    if "questions" not in st.session_state:
        st.session_state.questions = []
        st.session_state.current_q = 0
        st.session_state.feedback = []

    if st.button("Start Challenge"):
        with st.spinner("Generating questions..."):
            try:
                res = requests.post("http://localhost:8000/challenge/", json={"document": doc_text})
                qlist = res.json().get("questions", [])
                if qlist:
                    st.session_state.questions = qlist
                    st.session_state.current_q = 0
                    st.session_state.feedback = []
            except:
                st.error("Failed to generate challenge questions.")

    if st.session_state.questions:
        curr = st.session_state.current_q
        if curr < len(st.session_state.questions):
            question = st.session_state.questions[curr]
            st.markdown(f"**Q{curr+1}:** {question}")
            user_ans = st.text_area("Your Answer", key=f"answer_{curr}")

            if st.button("Submit Answer", key=f"submit_{curr}"):
                with st.spinner("Evaluating..."):
                    try:
                        payload = {
                            "document": doc_text,
                            "question": question,
                            "user_answer": user_ans
                        }
                        res = requests.post("http://localhost:8000/evaluate/", json=payload)
                        fb = res.json().get("feedback", "No feedback returned.")
                        st.session_state.feedback.append((question, user_ans, fb))
                        st.session_state.current_q += 1
                        st.experimental_rerun()
                    except:
                        st.error("Could not evaluate the answer.")

    if st.session_state.current_q == len(st.session_state.questions):
        st.success("Challenge Complete 👀")
        st.markdown("### 📝 Feedback Summary:")
        for i, (q, a, f) in enumerate(st.session_state.feedback, 1):
            st.markdown(f"**Q{i}:** {q}")
            st.markdown(f"_Your Answer:_ {a}")
            st.markdown(f"_Feedback:_ {f}")
            st.markdown("---")

