from pydantic import BaseModel

class DimensionsResponse(BaseModel):
    width: float   # Ancho calculado
    height: float  # Alto calculado
    unit: str      # Unidad de medida (ej: "cm" o "pixels")
    message: str   # Mensaje de éxito o error