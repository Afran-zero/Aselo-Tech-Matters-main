import uuid
from datetime import datetime
from typing import List
# Add to your existing imports
from ..models.form_model import FormData, FormSubmissionRequest
from ..controllers.form_controller import form_controller
from ..models.conversation_model import (
    ChatRequest, ChatResponse, ChatMessage, 
    AutoFillRequest, AutoFillResponse,
    SummaryRequest, SummaryResponse
)
from ..services.db_service import db_service
from ..services.llm_service import llm_service
from ..utils.error_handler import SessionNotFoundException, LLMException, DatabaseException
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ChatController:
    """Controller for handling chat-related business logic"""
    
    async def process_chat_message(self, request: ChatRequest) -> ChatResponse:
        """Process incoming chat message and generate bot response"""
        try:
            # Get existing conversation or create new one
            conversation = await db_service.get_conversation(request.sessionId)
            
            if conversation is None:
                logger.info(f"Creating new conversation for session: {request.sessionId}")
                messages = []
            else:
                messages = conversation.messages
            
            # Create user message
            user_message = ChatMessage(
                id=str(uuid.uuid4()),
                sender="user",
                message=request.message,
                timestamp=datetime.now()
            )
            
            # Add user message to conversation
            await db_service.add_message_to_conversation(request.sessionId, user_message)
            
            # Generate bot response using LLM
            bot_response_text = await llm_service.generate_chat_response(messages, request.message)
            
            # Create bot message
            bot_message = ChatMessage(
                id=str(uuid.uuid4()),
                sender="bot",
                message=bot_response_text,
                timestamp=datetime.now()
            )
            
            # Add bot message to conversation
            await db_service.add_message_to_conversation(request.sessionId, bot_message)
            
            logger.info(f"Processed chat message for session: {request.sessionId}")
            
            return ChatResponse(response=bot_response_text)
            
        except LLMException as e:
            logger.error(f"LLM error in chat processing: {e.message}")
            raise e
        except DatabaseException as e:
            logger.error(f"Database error in chat processing: {e.message}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error in chat processing: {str(e)}")
            raise DatabaseException(f"Failed to process chat message: {str(e)}")
    
    async def extract_form_data(self, request: AutoFillRequest) -> AutoFillResponse:
        """Extract structured form data from conversation and save to form database"""
        try:
            # Get conversation history
            conversation = await db_service.get_conversation(request.sessionId)
            
            if conversation is None or not conversation.messages:
                raise SessionNotFoundException(request.sessionId)
            
            # Extract form data using LLM
            form_data = await llm_service.extract_form_data(conversation.messages)
            
            # SAVE TO FORM DATABASE - NEW CODE
            await self._save_extracted_form_data(request.sessionId, form_data)
            
            logger.info(f"Extracted and saved form data for session: {request.sessionId}")
            
            return form_data
            
        except SessionNotFoundException as e:
            logger.error(f"Session not found for autofill: {request.sessionId}")
            raise e
        except LLMException as e:
            logger.error(f"LLM error in form extraction: {e.message}")
            raise e
        except DatabaseException as e:
            logger.error(f"Database error in form extraction: {e.message}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error in form extraction: {str(e)}")
            raise DatabaseException(f"Failed to extract form data: {str(e)}")

    async def _save_extracted_form_data(self, session_id: str, form_data: AutoFillResponse):
        """Save extracted form data to form database"""
        try:
            # Convert AutoFillResponse to FormData
            from ..models.form_model import FormData, FormSubmissionRequest
            
            form_data_obj = FormData(
                name=form_data.name,
                email=form_data.email,
                phone=form_data.phone,
                address=form_data.address,
                notes=form_data.notes
            )
            
            # Create form submission request
            form_request = FormSubmissionRequest(
                sessionId=session_id,
                formData=form_data_obj
            )
            
            # Save to form database
            await form_controller.submit_form(form_request)
            
        except Exception as e:
            logger.warning(f"Failed to save extracted form data for session {session_id}: {str(e)}")
            # Don't re-raise, we still want to return the extracted data even if save fails
    
    async def generate_summary(self, request: SummaryRequest) -> SummaryResponse:
        """Generate conversation summary"""
        try:
            # Get conversation history
            conversation = await db_service.get_conversation(request.sessionId)
            
            if conversation is None or not conversation.messages:
                raise SessionNotFoundException(request.sessionId)
            
            # Generate summary using LLM
            summary_text = await llm_service.generate_summary(conversation.messages)
            
            logger.info(f"Generated summary for session: {request.sessionId}")
            
            return SummaryResponse(summary=summary_text)
            
        except SessionNotFoundException as e:
            logger.error(f"Session not found for summary: {request.sessionId}")
            raise e
        except LLMException as e:
            logger.error(f"LLM error in summary generation: {e.message}")
            raise e
        except DatabaseException as e:
            logger.error(f"Database error in summary generation: {e.message}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error in summary generation: {str(e)}")
            raise DatabaseException(f"Failed to generate summary: {str(e)}")
    
    async def get_conversation_history(self, session_id: str) -> List[ChatMessage]:
        """Get conversation history for a session"""
        try:
            conversation = await db_service.get_conversation(session_id)
            
            if conversation is None:
                return []
            
            return conversation.messages
            
        except DatabaseException as e:
            logger.error(f"Database error getting conversation history: {e.message}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error getting conversation history: {str(e)}")
            raise DatabaseException(f"Failed to get conversation history: {str(e)}")


# Global chat controller instance
chat_controller = ChatController()