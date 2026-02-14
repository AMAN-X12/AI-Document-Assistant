from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


from app.services.llm import llm
from app.services.prompt import get_prompt
from app.services.memory import get_history


def chain():
    prompt = get_prompt()
    qa_chain = (
        {"context": RunnablePassthrough() ,
        "question": RunnablePassthrough(),
        "chat_history": lambda _: get_history(llm)
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return qa_chain
