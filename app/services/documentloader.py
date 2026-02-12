from langchain_community.document_loaders import TextLoader, PyPDFLoader
import re
from pathlib import Path
import tempfile
import fitz
# import pytesseract
# import io
# from PIL import Image
from langchain_core.documents import Document


# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' //for on testing phase



def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)



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
        # else:
        #     pix = page.get_pixmap(dpi=300)
        #     img = Image.open(io.BytesIO(pix.tobytes("png")))
        #     ocr_text = pytesseract.image_to_string(img)
        #     if ocr_text.strip():
        #      doc.append(Document(page_content=clean_text(ocr_text), metadata={"source": "ocr", "file_name": file_name, "page_number": page_num}))
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
            return documents
        else:
            raise ValueError(f"Unsupported file type: {file_suffix}")


    finally:
        Path(temp_file_path).unlink(missing_ok=True)




