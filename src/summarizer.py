import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load .env
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

llm = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct",
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.3,
)

def summarize(docs):
    text = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
Summarize the following news:

{text}

Give:
- Key Points
- Trends
- Final Summary
"""

    response = llm.invoke(prompt)
    return response.content