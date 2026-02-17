from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from app.services.engine import process_upload, ask_question



router = APIRouter()

class QuestionRequest(BaseModel):
    question: str


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
 try:
    if file.size > 10 * 1024 * 1024:
     raise HTTPException(status_code=400, detail="File too large")

    await process_upload(file)
    return {"message": "File uploaded  successfully."}
 except Exception as e :
    raise HTTPException(status_code=500, detail="error processing your file")


@router.post("/ask")
async def ask(request: QuestionRequest):
    response = await ask_question(request.question)
    return {"response": response}


