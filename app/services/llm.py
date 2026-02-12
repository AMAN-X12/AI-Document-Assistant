from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import key, modelid, llm_config

llm = ChatGoogleGenerativeAI(model=modelid, api_key=key, **llm_config)




