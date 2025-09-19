from fastapi import APIRouter, HTTPException
from typing import List

from ..models.form_model import (
    FormSubmissionRequest, FormSubmissionResponse, FormSubmission
)
from ..controllers.form_controller import form_controller
from ..utils.error_handler import AseloException
from ..utils.logger import get_logger

logger = get_logger(__name__)

# Create router instance
router = APIRouter(prefix="/api", tags=["forms"])


@router.post("/submitForm", response_model=FormSubmissionResponse, summary="Submit form data")
async def submit_form_endpoint(request: FormSubmissionRequest) -> FormSubmissionResponse:
    """
    Submit form data for a session.
    
    - **sessionId**: Unique session identifier
    - **formData**: Form data object containing user information
    
    Returns confirmation of successful form submission with submission ID.
    """
    try:
        logger.info(f"Processing form submission for session: {request.sessionId}")
        response = await form_controller.submit_form(request)
        return response
    
    except AseloException:
        # Re-raise custom exceptions to be handled by middleware
        raise
    except Exception as e:
        logger.error(f"Unexpected error in submit form endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/submission/{session_id}", response_model=FormSubmission, summary="Get form submission")
async def get_form_submission_endpoint(session_id: str) -> FormSubmission:
    """
    Get form submission for a specific session.
    
    - **session_id**: Unique session identifier
    
    Returns the form submission data if it exists.
    """
    try:
        logger.info(f"Getting form submission for session: {session_id}")
        submission = await form_controller.get_form_submission(session_id)
        return submission
    
    except AseloException:
        # Re-raise custom exceptions to be handled by middleware
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get form submission endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/submission/{session_id}/status", summary="Update form submission status")
async def update_form_status_endpoint(session_id: str, status: str) -> dict:
    """
    Update the status of a form submission.
    
    - **session_id**: Unique session identifier
    - **status**: New status for the submission
    
    Returns confirmation of status update.
    """
    try:
        logger.info(f"Updating form submission status for session: {session_id} to {status}")
        success = await form_controller.update_form_submission_status(session_id, status)
        
        if success:
            return {
                "success": True,
                "message": f"Form submission status updated to: {status}",
                "sessionId": session_id,
                "status": status
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to update form submission status")
    
    except AseloException:
        # Re-raise custom exceptions to be handled by middleware
        raise
    except Exception as e:
        logger.error(f"Unexpected error in update form status endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/submissions", response_model=List[str], summary="List all form submission session IDs")
async def list_form_submissions_endpoint() -> List[str]:
    """
    Get list of all form submission session IDs.
    
    Returns list of session IDs that have form submissions.
    """
    try:
        logger.info("Listing all form submissions")
        submissions = await form_controller.list_form_submissions()
        return submissions
    
    except AseloException:
        # Re-raise custom exceptions to be handled by middleware
        raise
    except Exception as e:
        logger.error(f"Unexpected error in list form submissions endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")