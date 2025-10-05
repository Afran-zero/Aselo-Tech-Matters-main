import uuid
from datetime import datetime
from typing import List

# Models
from ..models.form_model import (
    FormData,
    FormSubmissionRequest,
    Child,
    Category,
    Summary
)
from ..models.conversation_model import (
    ChatRequest,
    ChatResponse,
    ChatMessage,
    AutoFillRequest,
    AutoFillResponse,
    SummaryRequest,
    SummaryResponse
)

# Services & Controllers
from ..services.db_service import db_service
from ..services.llm_service import llm_service
from ..controllers.form_controller import form_controller

# Utils
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
        """Extract structured form data from conversation"""
        try:
            # Get conversation history
            conversation = await db_service.get_conversation(request.sessionId)
            
            if conversation is None or not conversation.messages:
                raise SessionNotFoundException(request.sessionId)
            
            # Extract form data using LLM
            form_data = await llm_service.extract_form_data(conversation.messages)
            
            # Optional: Save to form DB (comment out if not desired)
            # await self._save_extracted_form_data(request.sessionId, form_data)
            
            logger.info(f"Extracted form data for session: {request.sessionId}")
            
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
        """Save extracted form data to form database (optional helper)"""
        try:
            # Build Child object
            child = Child(
                firstName=form_data.firstName or "Unknown",
                lastName=form_data.lastName,
                gender=form_data.gender,
                age=form_data.age,
                streetAddress=form_data.streetAddress,
                parish=form_data.parish,
                phone1=form_data.phone1,
                phone2=form_data.phone2,
                nationality=form_data.nationality,
                schoolName=form_data.schoolName,
                gradeLevel=form_data.gradeLevel,
                livingSituation=form_data.livingSituation,
                vulnerableGroups=form_data.vulnerableGroups,
                region=form_data.region
            )

            # Create minimal FormData
            form_data_obj = FormData(
                child=child,
                category=Category(),  # empty for now
                summary=Summary(
                    callSummary="Auto-filled from conversation",
                    keepConfidential=True
                )
            )

            form_request = FormSubmissionRequest(
                sessionId=session_id,
                formData=form_data_obj
            )

            await form_controller.submit_form(form_request)

        except Exception as e:
            logger.warning(f"Failed to save extracted form data for session {session_id}: {str(e)}")
            # Do not re-raise — extraction should succeed even if save fails
    
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


# Global instance
chat_controller = ChatController()