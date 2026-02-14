from langchain_community.document_loaders import TextLoader
import re
from pathlib import Path
import tempfile
import fitz
from langchain_core.documents import Document





def clean_text(text:str):
    text=re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    text=re.sub(r'\s+'," ",text)
    return text.strip()


def pdf_reader(file_path,file_name):
    doc=[]
    pdf = fitz.open(file_path)

    for page_num, page in enumerate(pdf):
        text = page.get_text().strip()
        if text:
            doc.append(Document(page_content=clean_text(text), metadata={"file_name":file_name, "page_number": page_num, "source":"text"}))

    pdf.close()
    return doc



async def load_document(document):
    file_name=document.filename
    file_suffix=Path(file_name).suffix.lower()
    data = await document.read()
    with tempfile.NamedTemporaryFile(delete=False , suffix=file_suffix) as temp_file:

        temp_file.write(data)
        temp_file_path=temp_file.name

    try:
        if file_suffix=='.txt':
            loader=TextLoader(temp_file_path)
            documents=loader.load()
            for doc in documents:
              doc.page_content=clean_text(doc.page_content)
              doc.metadata['file_name']=file_name
            return documents
        elif file_suffix == '.pdf':
            documents = pdf_reader(temp_file_path, file_name)
            if not documents:
                raise ValueError("doesn't read scanned images .")
            return documents
        else:
            raise ValueError(f"Unsupported file type: {file_suffix}")


    finally:
        Path(temp_file_path).unlink(missing_ok=True)




