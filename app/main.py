from fastapi import FastAPI
from app.routes.DimensionsRoutes import router

app = FastAPI()

# Incluir las rutas del archivo DimensionsRoutes.py
app.include_router(router)
