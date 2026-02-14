---
title: AI Research Assistant
emoji: 😻
colorFrom: red
colorTo: indigo
sdk: gradio
sdk_version: 5.49.1
app_file: app.py
pinned: false
---

# AI Research Assistant 

A **Gradio-based** research assistant that turns a question into a structured, source-aware response (summary + key points + next steps). Designed as a lightweight “research copilot” you can run locally or deploy on Hugging Face Spaces.

### Design focus

This project focuses on retrieval-augmented research and verifiable synthesis rather than free-form text generation. The assistant separates information gathering from summarisation, encouraging grounded answers and traceable reasoning when scanning unfamiliar topics.

The goal is to demonstrate how lightweight LLM tools can support early-stage research while keeping outputs structured, concise, and easy to validate against primary sources.

## What it does
- Accepts a research question or topic prompt
- Produces a clear **summary** and **key takeaways**
- Suggests **follow-up questions** to deepen the investigation
- Generates a structured response you can copy into notes or a report

## Project structure
```text
.
├── app.py
├── requirements.txt
└── README.md
```

## Local development

### 1. Clone and install

```bash
git clone https://github.com/cicboy80/AI_RESEARCH_ASSISTANT.git
cd AI_RESEARCH_ASSISTANT
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

### 2. Environmental Variables

This project requires API keys for OpenAI and Tavily.

Set these as environment variables (recommended), or create a local `.env` file (**do not commit it**).

Required:

- OPENAI_API_KEY
- TAVILY_API_KEY

Example:

```bash
export OPENAI_API_KEY="..."
export TAVILY_API_KEY="..."
```

### 3. Run the app

```bash
python app.py
```

Then open the local Gradio URL printed in the terminal.

## Hugging Face Spaces: Secrets setup

Add the following under Settings → Secrets in your Space:

- OPENAI_API_KEY
- TAVILY_API_KEY

## Notes on security

- Never commit secrets (API keys, tokens, .env, certificates)
- Prefer platform secret managers (Hugging Face Secrets / cloud secret stores)

## License

Apache-2.0

