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
    max_tokens=400
)

def summarize(texts):
    text = "\n\n".join(texts)

    prompt = f"""
Summarize these news articles.

Return exactly this format:

Key Points:
- point
- point

Trends:
- trend

Overall Summary:
paragraph

News:
{text}
"""

    response = llm.invoke(prompt)
    return response.content