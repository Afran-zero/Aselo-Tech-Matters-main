from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import traceback
from typing import Union
from .logger import get_logger

logger = get_logger(__name__)


class AseloException(Exception):
    """Base exception class for Aselo application"""
    
    def __init__(self, message: str, status_code: int = 500, error_code: str = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or "INTERNAL_ERROR"
        super().__init__(self.message)


class DatabaseException(AseloException):
    """Exception for database-related errors"""
    
    def __init__(self, message: str, error_code: str = "DATABASE_ERROR"):
        super().__init__(message, 500, error_code)


class LLMException(AseloException):
    """Exception for LLM service-related errors"""
    
    def __init__(self, message: str, status_code: int = 500, error_code: str = "LLM_ERROR"):
        super().__init__(message, status_code, error_code)


class ValidationException(AseloException):
    """Exception for validation errors"""
    
    def __init__(self, message: str, error_code: str = "VALIDATION_ERROR"):
        super().__init__(message, 400, error_code)


class SessionNotFoundException(AseloException):
    """Exception for when session is not found"""
    
    def __init__(self, session_id: str):
        message = f"Session not found: {session_id}"
        super().__init__(message, 404, "SESSION_NOT_FOUND")


async def aselo_exception_handler(request: Request, exc: AseloException) -> JSONResponse:
    """Handle custom Aselo exceptions"""
    logger.error(f"Aselo exception: {exc.message} (Code: {exc.error_code})")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.message,
            "error_code": exc.error_code,
            "status_code": exc.status_code
        }
    )


async def http_exception_handler(request: Request, exc: Union[HTTPException, StarletteHTTPException]) -> JSONResponse:
    """Handle HTTP exceptions"""
    logger.error(f"HTTP exception: {exc.detail} (Status: {exc.status_code})")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "error_code": "HTTP_ERROR",
            "status_code": exc.status_code
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle validation exceptions"""
    logger.error(f"Validation error: {exc.errors()}")
    
    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "message": "Validation error",
            "error_code": "VALIDATION_ERROR",
            "status_code": 422,
            "details": exc.errors()
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "error_code": "INTERNAL_ERROR",
            "status_code": 500
        }
    )


def setup_exception_handlers(app):
    """Setup exception handlers for the FastAPI app"""
    app.add_exception_handler(AseloException, aselo_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)