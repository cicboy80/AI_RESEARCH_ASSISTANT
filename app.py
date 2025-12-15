# app.py — AI Research Assistant (Hugging Face-ready)

import os
import arxiv
import gradio as gr
from tavily import TavilyClient
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# ====== Environment Setup ======
# Hugging Face injects secrets automatically via Repo > Settings > Secrets
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ Missing OPENAI_API_KEY. Add it in Hugging Face → Settings → Secrets.")
if not TAVILY_API_KEY:
    raise ValueError("❌ Missing TAVILY_API_KEY. Add it in Hugging Face → Settings → Secrets.")

# ====== Initialize Clients ======
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, api_key=OPENAI_API_KEY)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

# ====== Search Functions ======
def search_web_tavily(query: str, k=5):
    """Search web using Tavily API."""
    res = tavily.search(query=query, max_results=k)
    return [
        f"[W{i}] {r['title']} ({r['url']})"
        for i, r in enumerate(res.get("results", [])[:k], start=1)
    ]

def search_arxiv(query: str, k=5):
    """Search research papers from arXiv API."""
    search = arxiv.Search(query=query, max_results=k)
    papers = []
    for i, r in enumerate(search.results(), start=1):
        # Extract and format publication date safely
        try:
            date = r.published.strftime("%Y-%m-%d")
        except Exception:
            date = "Unknown date"
        papers.append(f"[A{i}] {r.title} — Published: {date} — {r.pdf_url}")
    return papers

# ====== Summarization Logic ======
def summarize_research(query: str):
    """Combine Tavily + arXiv results and summarize them with inline citations."""
    if not query.strip():
        return "⚠️ Please enter a valid research topic."

    web_results = search_web_tavily(query)
    paper_results = search_arxiv(query)

    # Build structured context for the model
    context = f"""
Query: {query}

arXiv Papers:
{chr(10).join(paper_results) or '- None'}

Web Sources:
{chr(10).join(web_results) or '- None'}
"""

    # Define how to summarize content
    system_prompt = """
You are a precise academic research assistant.
Write a concise, structured summary of the topic in two sections:
1. Findings from arXiv Papers
2. Findings from Web Sources

Guidelines:
- Use bullet points.
- Cite each statement with the corresponding source ID (e.g., (A1), (W3)).
- If a paper includes a publication date, mention it in parentheses after the title.
- Do NOT invent IDs or include sources not in the list.
- Always include information from both arXiv and Web sources.
"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=context),
    ]

    # Generate summary
    response = llm.invoke(messages)

    # Combine results into readable markdown
    summary = f"### 🧠 Summary\n{response.content}\n\n**Sources:**\n" + \
              "\n".join(web_results + paper_results)

    return summary

# ====== Gradio Interface ======
with gr.Blocks(
    title="AI Research Assistant",
    theme=gr.themes.Soft(),
    css="#summary_box {max-height: 900px; overflow-y: auto; white-space: pre-wrap;}"
) as demo:
    gr.Markdown(
        """
        # 🧠 AI Research Assistant  
        Enter a research topic to generate a concise academic-style report with citations.
        """
    )

    query_input = gr.Textbox(
        label="Research Query",
        placeholder="e.g., Latest advancements in quantum computing",
        lines=2,
    )

    submit_btn = gr.Button("🔍 Search & Summarize")
    output = gr.Markdown(label="Summary", elem_id="summary_box", show_copy_button=True)

    submit_btn.click(summarize_research, inputs=query_input, outputs=output)

    gr.Markdown("---\nMade with ❤️ using OpenAI + LangChain + Tavily + Gradio\n")

# Launch for Hugging Face
demo.launch()
