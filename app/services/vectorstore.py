
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def create_vectorstore(documents):
      text_splitter=RecursiveCharacterTextSplitter(chunk_size=1200,chunk_overlap=210,is_separator_regex=False)
      text=text_splitter.split_documents(documents)
      embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
      vectorstore=FAISS.from_documents(text,embeddings)
      return vectorstore


