import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
import openai
import os

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("PDF OCR and Summary App")

uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_pdf:
    try:
        # Convert PDF to images
        images = convert_from_bytes(uploaded_pdf.read())
        st.write(f"Total pages: {len(images)}")

        # OCR each page and collect text
        full_text = ""
        with st.spinner("Performing OCR on PDF pages..."):
            for i, image in enumerate(images, start=1):
                text = pytesseract.image_to_string(image)
                st.text_area(f"Text extracted from page {i}", text, height=200)
                full_text += text + "\n"

        if full_text.strip():
            st.success("OCR completed successfully!")

            # Ask OpenAI to summarize the text
            with st.spinner("Generating summary with OpenAI..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                        {"role": "user", "content": f"Please provide a concise summary of the following text:\n\n{full_text}"}
                    ],
                    max_tokens=300,
                    temperature=0.7,
                )
                summary = response.choices[0].message.content
                st.header("Summary")
                st.write(summary)
        else:
            st.warning("No text extracted from the PDF.")

    except Exception as e:
        st.error(f"Error processing PDF: {e}")