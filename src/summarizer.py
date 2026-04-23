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
You are a professional news analyst.

Analyze the following news articles carefully and generate a high-quality summary.

Instructions:
- Remove duplicate or repetitive information
- Focus on factual insights
- Combine similar points
- Keep it concise but informative

Format:

Key Points:
- ...

Trends:
- ...

Final Summary:
...

News:
{text}
"""

    response = llm.invoke(prompt)
    return response.content