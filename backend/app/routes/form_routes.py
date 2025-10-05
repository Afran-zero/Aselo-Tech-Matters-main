from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

from ..models.form_model import (
    FormSubmissionRequest, FormSubmissionResponse, FormSubmission
)
from ..controllers.form_controller import form_controller
from ..utils.logger import get_logger

logger = get_logger(__name__)

# Create router instance
router = APIRouter(prefix="/api", tags=["forms"])


class UpdateStatusResponse(BaseModel):
    success: bool
    message: str
    sessionId: str
    status: str


@router.post("/submitForm", response_model=FormSubmissionResponse, summary="Submit form data")
async def submit_form_endpoint(request: FormSubmissionRequest) -> FormSubmissionResponse:
    """
    Submit form data for a session.
    
    - **sessionId**: Unique session identifier
    - **formData**: Form data object containing user information
    
    Returns confirmation of successful form submission with submission ID.
    """
    logger.info("Processing form submission", extra={"session_id": request.sessionId})
    return await form_controller.submit_form(request)


@router.get("/submission/{session_id}", response_model=FormSubmission, summary="Get form submission")
async def get_form_submission_endpoint(session_id: str) -> FormSubmission:
    """
    Get form submission for a specific session.
    
    - **session_id**: Unique session identifier
    
    Returns the form submission data if it exists.
    """
    logger.info("Getting form submission", extra={"session_id": session_id})
    return await form_controller.get_form_submission(session_id)


@router.put("/submission/{session_id}/status", response_model=UpdateStatusResponse, summary="Update form submission status")
async def update_form_status_endpoint(session_id: str, status: str) -> UpdateStatusResponse:
    """
    Update the status of a form submission.
    
    - **session_id**: Unique session identifier
    - **status**: New status for the submission
    
    Returns confirmation of status update.
    """
    logger.info("Updating form submission status", extra={"session_id": session_id, "status": status})
    success = await form_controller.update_form_submission_status(session_id, status)
    
    if not success:
        # This shouldn't happen in current logic, but guard anyway
        from ..utils.error_handler import AseloException
        raise AseloException("Failed to update form submission status", 500, "UPDATE_FAILED")
    
    return UpdateStatusResponse(
        success=True,
        message=f"Form submission status updated to: {status}",
        sessionId=session_id,
        status=status
    )


@router.get("/submissions", response_model=List[str], summary="List all form submission session IDs")
async def list_form_submissions_endpoint() -> List[str]:
    """
    Get list of all form submission session IDs.
    
    Returns list of session IDs that have form submissions.
    """
    logger.info("Listing all form submissions")
    return await form_controller.list_form_submissions()