from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from config import GEMINI_API_KEY, MODEL_NAME
from tools import TOOLS

SYSTEM="""You are Aditya360, an intelligent campus assistant.
Use tools when appropriate. Be concise, accurate and student-friendly.
Do not invent institutional facts. If verified information is unavailable, say so."""
llm=ChatGoogleGenerativeAI(model=MODEL_NAME,google_api_key=GEMINI_API_KEY)
agent=create_agent(model=llm,tools=TOOLS,system_prompt=SYSTEM)

def ask(question):
    r=agent.invoke({"messages":[{"role":"user","content":question}]})
    x=r["messages"][-1].content
    if isinstance(x,str): return x
    if isinstance(x,list):
        return "\n".join(b.get("text",str(b)) if isinstance(b,dict) else str(b) for b in x)
    return str(x)
