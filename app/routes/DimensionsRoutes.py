from fastapi import APIRouter, File, UploadFile
from app.controllers.DimensionsController import process_image
from app.model.DimensionsModel import DimensionsResponse

router = APIRouter()

@router.post("/upload", response_model=DimensionsResponse)
async def upload_image(image: UploadFile = File(...)):
    return await process_image(image)
