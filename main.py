from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()

from app.postes.router import router as postes_router
from app.auth.router import router as auth_router
from app.profil.router import router as profil_router

app = FastAPI(
    title="7Manager API",
    description="API de 7manager",
    version="1.0.0"
)

app.include_router(postes_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(profil_router, prefix="/api")
@app.get("/")
def root():
    return {"message": "API is running!", "docs": "/docs"}
