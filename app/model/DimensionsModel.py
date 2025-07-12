from pydantic import BaseModel

class DimensionsResponse(BaseModel):
    width: float   # Largo
    height: float  # Alto
    message: str   # Mensaje de éxito o error
