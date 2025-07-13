import streamlit as st
import requests

st.set_page_config(page_title="GEN-AI Assistant", layout="centered")

st.title("GEN-AI: Document Summary Assistant")

uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file:
    st.info("Generating summary, hold on please", icon="🧠")

    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    try:
        response = requests.post("http://localhost:8000/summarize/", files=files)
        result = response.json()
        summary = result.get("summary", "")

        st.subheader("Summary:")
        st.write(summary if summary else "No summary was generated.")
    except Exception as e:
        st.error("Failed to connect to the backend or process the file.")

