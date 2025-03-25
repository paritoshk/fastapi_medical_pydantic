import time
from typing import Any, Dict

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from app.services.openai_service import OpenAIService
from app.models.schema import MedicalQueryRequest

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging, LoggingRoute

# Setup logging
logger = setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Leo Medical Assistant API for healthcare providers",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    default_response_class=JSONResponse,
)

# Set all routes to use the custom LoggingRoute
app.router.route_class = LoggingRoute

# Mount static files directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Custom validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Custom handler for validation errors to provide more user-friendly error messages
    """
    errors = []
    for error in exc.errors():
        error_msg = {
            "loc": error.get("loc", []),
            "message": error.get("msg", ""),
            "type": error.get("type", "")
        }
        errors.append(error_msg)
    
    logger.warning(f"Validation error: {errors}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": errors, "message": "Validation error"},
    )

# Add startup and shutdown events
@app.on_event("startup")
async def startup_event():
    logger.info(" Starting Leo Medical Assistant API")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(" Shutting down Leo Medical Assistant API")

# Web UI routes
@app.get("/", response_class=HTMLResponse, tags=["ui"])
async def index(request: Request):
    """
    Serve the main web interface
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/ui/medical", response_class=HTMLResponse, tags=["ui"])
async def medical_ui(request: Request):
    """
    Serve the medical assistant interface
    """
    return templates.TemplateResponse("medical.html", {"request": request})

# Initialize OpenAI service for test endpoint
openai_service = OpenAIService()

# Test endpoint for LLM without authentication
@app.post("/test/llm", tags=["test"])
async def test_llm(query: MedicalQueryRequest):
    """
    Test endpoint for direct access to the OpenAI LLM without authentication.
    
    This endpoint allows direct testing of the medical query functionality without requiring
    user authentication. It's intended for development and testing purposes only and
    should not be exposed in production environments without proper security controls.
    
    Args:
        query (MedicalQueryRequest): The medical query containing patient information and the question.
        
    Returns:
        MedicalQueryResponse: A structured response containing the AI-generated medical advice,
            a disclaimer, model information, and usage statistics.
            
    Raises:
        HTTPException: 500 error if there's an issue processing the query.
        
    Examples:
        ```
        # Request
        POST /test/llm
        
        {
          "patient_info": {
            "age": 58,
            "gender": "female",
            "medical_history": ["osteoarthritis"],
            "current_medications": ["acetaminophen PRN"],
            "symptoms": ["joint pain", "stiffness in the morning"]
          },
          "query": "What non-pharmacological options might help with these symptoms?"
        }
        
        # Response
        {
          "response_id": "7845f214-9c1d-4fe7-b324-a8712e3f9bc1",
          "response": "For osteoarthritis with morning stiffness and joint pain...",
          "disclaimer": "MEDICAL DISCLAIMER: This information is provided by an AI assistant...",
          "model_used": "gpt-4o-mini",
          "created_at": "2025-03-24T18:32:43.511Z",
          "tokens_used": 380
        }
        ```
    """
    try:
        logger.info("Test LLM query received")
        response = await openai_service.process_medical_query(query)
        logger.info(f"Test LLM query processed successfully, response ID: {response.response_id}")
        return response
    except Exception as e:
        logger.error(f"Error processing test LLM query: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing test LLM query: {str(e)}",
        )

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint for the API
    """
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "0.1.0",
    }

# Root endpoint
@app.get("/root", tags=["root"])
async def root() -> Dict[str, Any]:
    """
    Root endpoint with API information
    """
    return {
        "name": settings.PROJECT_NAME,
        "docs": "/docs",
        "health": "/health",
        "version": "0.1.0",
    }