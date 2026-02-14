from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def get_prompt():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Use the following context {context} to answer the question in a beautiful way making points that are easy to read.don't start saying based on your given context start with the answer directly. If the question is not related to the context, simply say you don't know. Make sure to use the context to answer the question and don't make up answers. If the question is not clear, ask for clarification"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human","{question}")
    ])
    return prompt