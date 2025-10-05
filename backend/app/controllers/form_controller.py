import uuid
from datetime import datetime

from ..models.form_model import (
    FormSubmissionRequest, FormSubmissionResponse, FormSubmission, FormData
)
from ..services.db_service import db_service
from ..utils.error_handler import DatabaseException, ValidationException
from ..utils.logger import get_logger

logger = get_logger(__name__)


class FormController:
    """Controller for handling form-related business logic"""
    
    async def submit_form(self, request: FormSubmissionRequest) -> FormSubmissionResponse:
        """Submit form data for a session"""
        try:
            # Validate form data
            self._validate_form_data(request.formData)
            
            # Generate unique submission ID
            submission_id = str(uuid.uuid4())
            
            # Create form submission
            form_submission = FormSubmission(
                sessionId=request.sessionId,
                submissionId=submission_id,
                formData=request.formData,
                submitted_at=datetime.now(),
                status="submitted"
            )
            
            # Save to database
            await db_service.save_form_submission(form_submission)
            
            logger.info(f"Form submitted successfully for session: {request.sessionId}")
            
            return FormSubmissionResponse(
                success=True,
                message="Form submitted successfully",
                submissionId=submission_id
            )
            
        except ValidationException as e:
            logger.error(f"Validation error in form submission: {e.message}")
            raise e
        except DatabaseException as e:
            logger.error(f"Database error in form submission: {e.message}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error in form submission: {str(e)}")
            raise DatabaseException(f"Failed to submit form: {str(e)}")
    
    async def get_form_submission(self, session_id: str) -> FormSubmission:
        """Get form submission for a session"""
        try:
            submission = await db_service.get_form_submission(session_id)
            
            if submission is None:
                raise ValidationException(f"No form submission found for session: {session_id}")
            
            return submission
            
        except ValidationException as e:
            logger.error(f"Form submission not found: {session_id}")
            raise e
        except DatabaseException as e:
            logger.error(f"Database error getting form submission: {e.message}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error getting form submission: {str(e)}")
            raise DatabaseException(f"Failed to get form submission: {str(e)}")
    
    async def update_form_submission_status(self, session_id: str, status: str) -> bool:
        """Update form submission status"""
        try:
            # Get existing submission
            submission = await db_service.get_form_submission(session_id)
            
            if submission is None:
                raise ValidationException(f"No form submission found for session: {session_id}")
            
            # Update status
            submission.status = status
            
            # Save updated submission
            await db_service.save_form_submission(submission)
            
            logger.info(f"Updated form submission status for session {session_id}: {status}")
            
            return True
            
        except ValidationException as e:
            logger.error(f"Validation error updating form status: {e.message}")
            raise e
        except DatabaseException as e:
            logger.error(f"Database error updating form status: {e.message}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error updating form status: {str(e)}")
            raise DatabaseException(f"Failed to update form submission status: {str(e)}")
    
    def _validate_form_data(self, form_data: FormData):
        """Validate form data"""
        # Validate phone formats if provided
        if form_data.child.phone1:
            if not self._is_valid_phone(form_data.child.phone1):
                raise ValidationException("Invalid format for Phone #1")
        
        if form_data.child.phone2:
            if not self._is_valid_phone(form_data.child.phone2):
                raise ValidationException("Invalid format for Phone #2")
        
        logger.info("Form data validation passed")
    
    def _is_valid_phone(self, phone: str) -> bool:
        """Basic phone validation - allows various formats"""
        import re
        # Remove common separators
        cleaned_phone = re.sub(r'[\s\-\(\)\+]', '', phone)
        # Check if it's all digits and reasonable length
        return cleaned_phone.isdigit() and 10 <= len(cleaned_phone) <= 15
    
    async def list_form_submissions(self) -> list:
        """Get list of all form submission session IDs"""
        try:
            return await db_service.list_form_submissions()
        except DatabaseException as e:
            logger.error(f"Database error listing form submissions: {e.message}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error listing form submissions: {str(e)}")
            raise DatabaseException(f"Failed to list form submissions: {str(e)}")


# Global form controller instance
form_controller = FormController()