from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class FormData(BaseModel):
    """Model for form data"""
    name: Optional[str] = Field(None, description="User name")
    email: Optional[str] = Field(None, description="User email")
    phone: Optional[str] = Field(None, description="User phone number")
    address: Optional[str] = Field(None, description="User address")
    notes: Optional[str] = Field(None, description="Additional notes")
    # Allow for additional fields that might be added later
    additional_fields: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional form fields")


class FormSubmissionRequest(BaseModel):
    """Model for form submission requests"""
    sessionId: str = Field(..., description="Session identifier")
    formData: FormData = Field(..., description="Form data to submit")


class FormSubmissionResponse(BaseModel):
    """Model for form submission responses"""
    success: bool = Field(..., description="Submission success status")
    message: str = Field(..., description="Confirmation message")
    submissionId: str = Field(..., description="Unique submission identifier")


class FormSubmission(BaseModel):
    """Model for stored form submissions"""
    sessionId: str = Field(..., description="Session identifier")
    submissionId: str = Field(..., description="Unique submission identifier")
    formData: FormData = Field(..., description="Submitted form data")
    submitted_at: datetime = Field(default_factory=datetime.now, description="Submission timestamp")
    status: str = Field(default="submitted", description="Submission status")