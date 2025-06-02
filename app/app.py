from fastapi import FastAPI

from app.routes.routes import router

app = FastAPI(
    title="Embrapa Vitivinicultura API",
    description="API para consulta de dados de vitivinicultura da Embrapa.",
    version="1.0",
)

app.include_router(router, prefix="/api/v1", tags=["Vitivinicultura"])
