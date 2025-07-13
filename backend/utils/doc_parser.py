import fitz  

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    this will pull raw text out of a PDF file.
    also accept file as byte stream (from upload or API).
    """
    text = []
    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for page in doc:
                page_text = page.get_text()
                if page_text:
                    text.append(page_text.strip())
    except Exception:
        pass  # so i let the caller decide how to handle bad file
    return "\n".join(text)

def extract_text_from_txt(file_bytes: bytes) -> str:
    """
    it will read plain .txt file from bytes.
    it skip over encoding issue silently.
    """
    try:
        return file_bytes.decode("utf-8", errors="ignore")
    except Exception:
        return ""

