
from app.services.documentloader import load_document
from app.services.vectorstore import create_vectorstore
from app.services.chain import chain
from app.services.memory import add_messages




vectorstore=None
qa_chain=None

try:

  async def process_upload(uploaded_file):
      global vectorstore,qa_chain
      docs = await load_document(uploaded_file)
      vectorstore=create_vectorstore(docs)
      retriever=vectorstore.as_retriever(search_kwargs={"k": 4})
      qa_chain= chain(retriever)


  async def ask_question(question):
        if qa_chain is None:
            raise Exception("Document not uploaded. Please upload a document first.")
        try:
           response = await qa_chain.ainvoke(question)
        except Exception :
           raise  Exception("make sure you are connected to the internet")
        add_messages(question, response)
        return response
except Exception as e:
      print("oops can't proceed now : ", str(e))
