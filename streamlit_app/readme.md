# How to Run Your Streamlit App

Inside your script, you can access command-line arguments via `sys.argv`.

---

## Summary Table

*Note:* `--network="host"` allows your container to reach the Ollama API on localhost.

---

## Summary Table

| Step                     | Command / Action                                   |
|--------------------------|--------------------------------------------------|
| Pull Ollama Docker Image | `docker pull ollama/ollama:latest`                |
| Run Ollama Container     | `docker run -d --name ollama -p 11434:11434 -v ollama:/root/.ollama ollama/ollama:latest` |
| Pull Gemma Model         | `docker exec -it ollama ollama pull gemma3:4b`   |
| Setup Python venv        | `python3 -m venv venv && source venv/bin/activate`|
| Install Python deps      | `pip install ollama requests`                      |
| Run Python app           | `python app.py`                                    |

---

## References

- [Deploy Gemma 2 with Ollama & Docker](https://www.oneclickitsolution.com/centerofexcellence/aiml/deploy-gemma-2-with-ollama-docker)
- [Run Gemma 3 Locally with Ollama and Python](https://www.datacamp.com/tutorial/gemma-3-ollama)
- [Ollama GitHub Repository](https://github.com/ollama/ollama)

---

## Contact & Support

For advanced usage, integration with ADK, or troubleshooting, refer to official Ollama docs or community forums.

---

*This README was generated to help you quickly set up a local GPT environment using Ollama, Gemma, Docker, and Python.*



| Step                     | Command Example                                               |
|--------------------------|---------------------------------------------------------------|
| Navigate to project      | `cd ~/projects`                                               |
| Run Streamlit app        | `streamlit run ai_agent_build/streamlit_app/ai_agent_built.py` |
| Run as Python module     | `python -m streamlit run ai_agent_build/streamlit_app/ai_agent_built.py` |
| Pass arguments           | `streamlit run app.py -- arg1 arg2`                           |

---

## References

- [Streamlit Docs: Run your app](https://docs.streamlit.io/develop/concepts/architecture/run-your-app)
- [Streamlit CLI Reference](https://docs.streamlit.io/develop/api-reference/cli/run)
- [Running Streamlit from Python script](https://ploomber.io/blog/streamlit-from-python/)

---

*This README section helps you quickly run your Streamlit app locally.*
