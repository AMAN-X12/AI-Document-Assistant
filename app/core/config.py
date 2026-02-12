from dotenv import load_dotenv
import os

load_dotenv()


key=os.getenv("key")
modelid="gemini-2.5-flash"
llm_config  ={
    "temperature": 0.5,
    "max_output_tokens": 700,
    "top_p": 0.95,
    "top_k": 40,
}
