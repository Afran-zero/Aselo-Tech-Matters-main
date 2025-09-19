from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ChatMessage(BaseModel):
    """Model for individual chat messages"""
    id: str = Field(..., description="Unique message ID")
    sender: str = Field(..., description="Message sender: 'user' or 'bot'")
    message: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")


class ChatRequest(BaseModel):
    """Model for incoming chat requests"""
    sessionId: str = Field(..., description="Session identifier")
    message: str = Field(..., description="User message content")


class ChatResponse(BaseModel):
    """Model for chat responses"""
    response: str = Field(..., description="Bot response message")


class ConversationHistory(BaseModel):
    """Model for conversation history"""
    sessionId: str = Field(..., description="Session identifier")
    messages: List[ChatMessage] = Field(default_factory=list, description="List of messages")
    created_at: datetime = Field(default_factory=datetime.now, description="Session creation time")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update time")


class AutoFillRequest(BaseModel):
    """Model for autofill requests"""
    sessionId: str = Field(..., description="Session identifier")


class AutoFillResponse(BaseModel):
    """Model for autofill responses"""
    name: Optional[str] = Field(None, description="Extracted name")
    email: Optional[str] = Field(None, description="Extracted email")
    phone: Optional[str] = Field(None, description="Extracted phone number")
    address: Optional[str] = Field(None, description="Extracted address")
    notes: Optional[str] = Field(None, description="Additional notes")


class SummaryRequest(BaseModel):
    """Model for summary requests"""
    sessionId: str = Field(..., description="Session identifier")


class SummaryResponse(BaseModel):
    """Model for summary responses"""
    summary: str = Field(..., description="Conversation summary")