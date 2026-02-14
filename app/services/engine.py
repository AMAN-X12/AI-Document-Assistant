
from app.services.documentloader import load_document
from app.services.chain import chain
from app.services.memory import add_messages
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.services.embeddings import get_embeddings
import numpy as np


document=[]
embeddings=[]
qa_chain = None

try:

  async def process_upload(uploaded_file):
      global document, embeddings

      docs = await load_document(uploaded_file)

      text_splitter=  RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=250)
      chunks=text_splitter.split_documents(docs)

      document=[]
      embeddings=[]

      for chunk in chunks:
          document.append(chunk)
          embeddings.append(get_embeddings(chunk.page_content))


  async def ask_question(question):
        if not document:
            raise Exception("Document not uploaded. Please upload a document first.")
        try:
           question_embedding = get_embeddings(question)
           similarities=[]


           for emb in embeddings:
               sim=np.dot(question_embedding, emb) / (np.linalg.norm(question_embedding) * np.linalg.norm(emb))
               similarities.append(sim)

           top_k_indices = np.argsort(similarities)[-4:][::-1]
           relevant_chunks = [document[i] for i in top_k_indices]
           context=" ".join([chunk.page_content for chunk in relevant_chunks])
           qa_chain = chain()
           response = await qa_chain.ainvoke({
               "context":context,
               "question":question
           })
        except Exception :
           raise  Exception("make sure you are connected to the internet")
        add_messages(question, response)
        return response
except Exception as e:
      print("oops can't proceed now : ", str(e))
