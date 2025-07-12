from app.services.DimensionsService import calculate_dimensions
from fastapi import HTTPException, UploadFile

# Controlador para recibir y procesar la imagen
async def process_image(image: UploadFile):
    try:
        dimensions = await calculate_dimensions(image.file)
        return dimensions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
