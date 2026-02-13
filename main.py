# from app.services.documentloader import load_document
# from app.services.vectorstore import create_vectorstore
# from app.services.chain import chain
# from app.services.memory import add_messages






# print("Hey 👋 I am Your END TO END RAG AI Assistant. How can I help you?")
# try:
#  file_path = input("Enter document path (PDF/TXT): ")
#  with open(file_path, "rb") as uploaded_file:
#      docs = load_document(uploaded_file)


#  vectorstore=create_vectorstore(docs)
#  retriever=vectorstore.as_retriever(search_kwargs={"k":2})
#  qa_chain=chain(retriever)


#  while True:
#     question = input("You: ")
#     if question.lower() == "exit":
#         break
#     try:
#      response = qa_chain.invoke(question)
#     except Exception :
#         raise  Exception("make sure you are connected to the internet")
#     add_messages(question, response)
#     print("AI:", response)
# except Exception as e:
#     print("oops can't proceed now : ", str(e))




from fastapi import FastAPI
from app.api.routes import router
import uvicorn
import os
app = FastAPI(title=" End-to-End RAG AI Assistant", description="An AI assistant that can answer questions based on uploaded documents.")
app.include_router(router)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)