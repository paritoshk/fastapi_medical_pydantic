from fastapi import APIRouter

from app.api.endpoints import auth, medical

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(medical.router, prefix="/medical", tags=["medical"])