from fastapi import APIRouter, HTTPException
from typing import List
from fastapi.responses import JSONResponse

from ..models.conversation_model import (
    ChatRequest, ChatResponse, ChatMessage,
    AutoFillRequest, AutoFillResponse,
    SummaryRequest, SummaryResponse
)
from ..controllers.chat_controller import chat_controller
from ..utils.error_handler import AseloException
from ..utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


def success_response(data):
    """Helper to wrap responses for frontend compatibility"""
    return JSONResponse(content={"success": True, "data": data})


@router.post("/chat", response_model=ChatResponse, summary="Process chat message")
async def chat_endpoint(request: ChatRequest):
    try:
        logger.info(f"Processing chat request for session: {request.sessionId}")
        response = await chat_controller.process_chat_message(request)
        return success_response(response.model_dump())
    
    except AseloException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


# In chat_routes.py - ensure this endpoint exists
@router.post("/autofill", response_model=AutoFillResponse, summary="Extract form data from conversation")
async def autofill_form_data(request: AutoFillRequest) -> AutoFillResponse:
    """
    Extract form data from conversation history.
    
    - **sessionId**: Session identifier to extract data from
    
    Returns extracted form data in structured format.
    """
    try:
        logger.info(f"Extracting form data for session: {request.sessionId}")
        response = await chat_controller.extract_form_data(request)
        return success_response(response.model_dump())
    
    except AseloException:
        raise
    except Exception as e:
        logger.error(f"Error in form data extraction: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to extract form data")


@router.post("/summarize", response_model=SummaryResponse, summary="Generate conversation summary")
async def summarize_endpoint(request: SummaryRequest):
    try:
        logger.info(f"Processing summary request for session: {request.sessionId}")
        response = await chat_controller.generate_summary(request)
        return success_response(response.dict())
    
    except AseloException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in summary endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/conversation/{session_id}", response_model=List[ChatMessage], summary="Get conversation history")
async def get_conversation_endpoint(session_id: str):
    try:
        logger.info(f"Getting conversation history for session: {session_id}")
        messages = await chat_controller.get_conversation_history(session_id)
        return success_response([msg.dict() for msg in messages])
    
    except AseloException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get conversation endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
                   