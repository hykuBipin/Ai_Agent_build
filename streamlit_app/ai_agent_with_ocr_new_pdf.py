import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
import os
from multiprocessing import Pool, cpu_count
from openai import OpenAI

# Setup OpenAI client
api_key = os.getenv("OPENAI_API_KEY") or "sk-proj-..."  # Replace with your actual key or set as env variable
client = OpenAI(api_key=api_key)

st.title("Uniken PDF OCR + Custom Prompt Summary")

# File uploader
uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])

# Prompt input
custom_prompt = st.text_area(
    "Enter your custom prompt for summarization or analysis:",
    "Please summarize the following text concisely.",
    height=100
)

# OCR function for multiprocessing
def ocr_image(image):
    return pytesseract.image_to_string(image)

if uploaded_pdf:
    try:
        # Convert PDF pages to images
        images = convert_from_bytes(uploaded_pdf.read())
        total_pages = len(images)
        st.write(f"Total pages: {total_pages}")

        # Handle page limit safely
        default_pages = min(10, total_pages)
        max_pages = st.number_input("Limit number of pages to OCR (0 = all)", 0, total_pages, default_pages)

        if st.button("Start OCR and Summarization"):
            selected_images = images if max_pages == 0 else images[:max_pages]

            with st.spinner("Performing OCR in parallel..."):
                with Pool(processes=min(cpu_count(), len(selected_images))) as pool:
                    ocr_results = pool.map(ocr_image, selected_images)

            full_text = "\n".join(ocr_results)

            if full_text.strip():
                st.success("OCR completed successfully!")

                with st.spinner("Generating response with OpenAI..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": f"{custom_prompt}\n\n{full_text}"}
                        ],
                        max_tokens=500,
                        temperature=0.7,
                    )
                    summary = response.choices[0].message.content
                    st.header("AI Response")
                    st.write(summary)
            else:
                st.warning("No text extracted from the PDF.")

    except Exception as e:
        st.error(f"Error processing PDF: {e}")