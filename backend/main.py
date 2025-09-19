import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv; load_dotenv()
import logging
logging.basicConfig(level=logging.DEBUG)  # Or INFO/ERROR as needed
# Load environment variables from .env file

load_dotenv()

from app.routes.chat_routes import router as chat_router
from app.routes.form_routes import router as form_router
from app.utils.error_handler import setup_exception_handlers
from app.utils.logger import get_logger, setup_logger

# Setup logging
logger = setup_logger("aselo_main", "INFO")

# Create FastAPI application
app = FastAPI(
    title="Aselo Backend API",
    description="A modular FastAPI backend for chatbot and form processing with OpenRouter LLM integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup exception handlers
setup_exception_handlers(app)

# Include routers
app.include_router(chat_router)
app.include_router(form_router)


@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Aselo Backend API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "chat": "/api/chat",
            "autofill": "/api/autofill", 
            "summarize": "/api/summarize",
            "submit_form": "/api/submitForm",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=dict)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2025-09-15T00:00:00Z",
        "services": {
            "database": "operational",
            "llm": "operational" if os.getenv("OPENROUTER_API_KEY") else "configuration_required"
        }
    }


if __name__ == "__main__":
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8001))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    logger.info(f"Starting Aselo Backend API on {host}:{port}")
    logger.info(f"OpenRouter API Key configured: {'Yes' if os.getenv('OPENROUTER_API_KEY') else 'No'}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
