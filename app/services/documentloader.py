from langchain_community.document_loaders import TextLoader
import re
from pathlib import Path
import tempfile
import fitz
from langchain_core.documents import Document
from PIL import Image
import json
from google.cloud import vision
import io
from app.core.config import creds_json
from google.oauth2 import service_account



def get_vision_client():

    if not creds_json:
        raise ValueError("Google credentials not found in environment variables.")

    credentials = service_account.Credentials.from_service_account_info(
        json.loads(creds_json)
    )

    return vision.ImageAnnotatorClient(credentials=credentials)


def extract_text_from_image(image_bytes):
    client = get_vision_client

    image = vision.Image(content=image_bytes)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description
    return ""


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
        else:
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            ocr_text = extract_text_from_image(img)
            if ocr_text.strip():
             doc.append(Document(page_content=clean_text(ocr_text), metadata={"source": "ocr", "file_name": file_name, "page_number": page_num}))

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




