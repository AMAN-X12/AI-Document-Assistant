from langchain_core.messages import trim_messages , HumanMessage, SystemMessage, AIMessage


history=[]
def add_messages(user,ai ):
    history.append(HumanMessage(content=user))
    history.append(AIMessage(content=ai))

def get_history(llm):
    return trim_messages(
        messages=history,
        max_tokens=400,
        strategy="last",
        token_counter=llm,
        include_system=True,
        start_on="human",
    )

