import streamlit as st
import requests
import json
from PyPDF2 import PdfReader

st.title("Dost - Local Chatbot with Gemma + Ollama")

uploaded_pdf = st.file_uploader("Upload your PDF", type="pdf")
prompt = st.text_area("Enter your prompt (or leave empty to summarize the PDF):")

pdf_text = ""
if uploaded_pdf is not None:
    reader = PdfReader(uploaded_pdf)
    pages_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages_text.append(text)
    pdf_text = "\n".join(pages_text)
    if pdf_text.strip():
        st.success("PDF uploaded and text extracted!")
        st.text_area("Extracted PDF Text Preview", pdf_text, height=300)
    else:
        st.error("Failed to extract meaningful text from PDF. If this is a scanned document, OCR is needed.")

if st.button("Send"):
    with st.spinner("Generating response..."):
        # Construct prompt: if user prompt is empty, generate summary prompt
        if pdf_text.strip() == "":
            st.error("No PDF text extracted to process.")
        else:
            # Compose a prompt that explicitly asks for summary if user prompt empty
            user_instruction = prompt.strip() or "Please provide a concise summary of the above PDF content."
            combined_prompt = f"Here is the content extracted from a PDF document:\n\n{pdf_text}\n\nUser: {user_instruction}\nAssistant:"

            # Make request to your local API
            try:
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "gemma:2b",
                        "prompt": combined_prompt,
                        "stream": True
                    },
                    stream=True,
                    timeout=60,
                )
                output = ""
                placeholder = st.empty()
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line.decode("utf-8"))
                            output += data.get("response", "")
                            placeholder.markdown(output)
                        except json.JSONDecodeError:
                            # ignore or log bad json line
                            continue
                st.success("Response generated successfully!")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the API: {e}")