import streamlit as st
import requests
import json

st.title("Dost - Local Chatbot with Gemma + Ollama")

prompt = st.text_area("Enter your prompt:")

if st.button("Send"):
    with st.spinner("Generating response..."):
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma:2b",
                "prompt": prompt,
                "stream": True
            },
            stream=True
        )
        
        output = ""
        placeholder = st.empty()  # placeholder to update the response live

        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    output += data.get("response", "")
                    placeholder.markdown(output)  # update output in real time
                except json.JSONDecodeError as e:
                    st.error(f"Failed to decode: {e}")
        
        st.success("Response generated successfully!")