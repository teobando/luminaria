from fastapi import FastAPI
from app.routes.DimensionsRoutes import router

app = FastAPI()

# Include routes from the DimensionsRoutes module
app.include_router(router)
