from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Meta's Llama API exposes an OpenAI-compatible endpoint, so we can reuse
# ChatOpenAI and just point it at Meta's base_url + key instead of OpenAI's.
META_BASE_URL = "https://api.llama.com/compat/v1/"


def load_llm(engine: str = "groq"):
    """
    engine: "groq" or "meta"
    Keeping this as one function (instead of two model files) means every
    service just asks for an engine by name and doesn't need to know
    anything about how each provider is wired up.
    """
    engine = (engine or "groq").lower()

    if engine == "meta":
        return ChatOpenAI(
            api_key=os.getenv("LLAMA_API_KEY"),
            base_url=META_BASE_URL,
            model=os.getenv("LLAMA_MODEL", "Llama-4-Maverick-17B-128E-Instruct-FP8"),
            temperature=0.7,
        )

    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="openai/gpt-oss-120b",
        temperature=0.7,
    )
