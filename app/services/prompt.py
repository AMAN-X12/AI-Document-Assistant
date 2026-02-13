from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def get_prompt():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Use the following context {context} to answer the question in a beautiful way making points that are easy to read. If the answer isn't in the context, say you don't know."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human","{question}")
    ])
    return prompt