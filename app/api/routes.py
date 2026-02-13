from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel
from app.services.engine import process_upload, ask_question



router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    await process_upload(file)
    return {"message": "File uploaded  successfully."}


@router.post("/ask")
async def ask(request: QuestionRequest):
    response = await ask_question(request.question)
    return {"response": response}

@router.get("/healthz")
async def get_status():
    return {"status": "API is running successfully."}

