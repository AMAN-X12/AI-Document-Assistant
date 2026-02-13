
vectorstore = None
qa_chain = None

async def process_upload(uploaded_file):
    global vectorstore, qa_chain
    try:
        from app.services.documentloader import load_document
        from app.services.vectorstore import create_vectorstore
        from app.services.chain import chain

        docs = await load_document(uploaded_file)
        vectorstore = create_vectorstore(docs)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
        qa_chain = chain(retriever)
    except Exception as e:
        print(f"Error during upload processing: {e}")
        raise e

async def ask_question(question):
    if qa_chain is None:
        return "Please upload a document first!"

    try:
        from app.services.memory import add_messages
        response = await qa_chain.ainvoke(question)
        add_messages(question, response)
        return response
    except Exception as e:
        print(f"Error during Q&A: {e}")
        return "I'm having trouble connecting to the internet. Please try again."