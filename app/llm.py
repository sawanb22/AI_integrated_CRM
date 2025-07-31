import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

def get_llm(model: str | None = None) -> ChatGroq:
    api_key = os.getenv("GROQ_API_KEY")
    model_name = model or os.getenv("GROQ_MODEL", "gemma-2-9b-it")  # ✅ updated default

    if not api_key:
        raise RuntimeError("❌ GROQ_API_KEY is not set in the environment")

    return ChatGroq(
        api_key=api_key,
        model_name=model_name,  # ✅ correct keyword arg for langchain_groq
        temperature=0
    )
