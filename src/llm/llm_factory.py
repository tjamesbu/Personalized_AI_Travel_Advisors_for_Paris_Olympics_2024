import os
from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel

load_dotenv()

provider: str = os.getenv("LLM_PROVIDER")
model: str = os.getenv("LLM_MODEL")


def get_llm() -> BaseChatModel:
    match provider:
        case "openai":
            # Note: Import is done here to improve loading time, at the cost of readability
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(model=model, temperature=0.1)
        case "google":
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(model=model)
        case "groq":
            from langchain_groq import ChatGroq
            llm = ChatGroq(model_name=model)
        case _:
            raise ValueError
    return llm

