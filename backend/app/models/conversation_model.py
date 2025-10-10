from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from typing import Literal
from datetime import datetime

# Reuse Literal types from form.model for consistency
# To avoid circular imports, we redefine the Literals here (or better: move to shared enums)
# For now, we duplicate for correctness and clarity

# --- Shared Literal Definitions (mirroring form.model.py) ---

CHILD_GENDER = Literal["Male", "Female", "Other", "Unknown"]

CHILD_AGE = Literal[
    "Unborn", "0", "01", "02", "03", "04", "05", "06", "07", "08", "09",
    "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
    "21", "22", "23", "24", "25", ">25", "Unknown"
]

PARISH = Literal[
    "Kingston", "St. Andrew", "St. Thomas", "St. Catherine", "Clarendon", "Manchester",
    "St. Elizabeth", "Westmoreland", "Hanover", "St. James", "Trelawny", "St. Ann",
    "St. Mary", "Portland", "Unknown"
]

LIVING_SITUATION = Literal[
    "Alternative care", "Group residential facility", "Homeless or marginally housed",
    "In detention", "Living independently", "With parent(s)", "With relatives", "Other", "Unknown"
]

VULNERABLE_GROUPS = Literal[
    "Child in conflict with the law", "Child living in conflict zone", "Child living in poverty",
    "Child member of an ethnic, racial or religious minority", "Child on the move (involuntarily)",
    "Child on the move (voluntarily)", "Child with disability", "LGBTQI+/SOGIESC child",
    "Out-of-school child", "Other"
]

REGION = Literal["Unknown", "Cities", "Rural areas", "Town & semi-dense areas"]

LOCATION_OF_ISSUE = Literal[
    "Unknown", "Home (own)", "Home (other)", "Educational Establishment", "Institution",
    "Online", "Public place", "Other"
]

ACTION_TAKEN = Literal[
    "Direct interventions by the child helpline", "Provision of information about SafeSpot",
    "Recommendations of resources", "Recommendation that young person contact SafeSpot",
    "Referrals to child protection agencies", "Referrals to law enforcement agencies",
    "Referrals to general healthcare professionals", "Referrals to mental health services",
    "Referrals to other organisations", "Referrals to school counsellors",
    "Reports to Child Sexual Abuse Material"
]

OUTCOME_OF_CONTACT = Literal["Resolved", "Follow up by next shift", "Follow up with external entity"]

HOW_KNOWN = Literal[
    "AI", "Advertisement", "Social media", "SMS/Text Message", "Traditional Media", "Word of Mouth"
]


# --- Models ---

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
    """Model for autofill responses — aligned with form.model.py types"""
    firstName: Optional[str] = Field(None, description="Extracted first name")
    lastName: Optional[str] = Field(None, description="Extracted last name")
    gender: Optional[CHILD_GENDER] = Field(None, description="Extracted gender")
    age: Optional[CHILD_AGE] = Field(None, description="Extracted age")
    streetAddress: Optional[str] = Field(None, description="Extracted street address")
    parish: Optional[PARISH] = Field(None, description="Extracted parish")
    phone1: Optional[str] = Field(None, description="Extracted phone #1")
    phone2: Optional[str] = Field(None, description="Extracted phone #2")
    nationality: Optional[str] = Field(None, description="Extracted nationality")
    schoolName: Optional[str] = Field(None, description="Extracted school name")
    gradeLevel: Optional[str] = Field(None, description="Extracted grade level")
    livingSituation: Optional[LIVING_SITUATION] = Field(None, description="Extracted living situation")
    vulnerableGroups: Optional[List[VULNERABLE_GROUPS]] = Field(None, description="Extracted vulnerable groups")
    region: Optional[REGION] = Field(None, description="Extracted region")
    # Suggested categories based on conversation
    suggested_categories: Optional[Dict[str, List[str]]] = Field(
        None,
        description="Suggested categories and subcategories (keys match Category field names)"
        
    )
    summary: Optional[Dict[str, Any]] = Field(
    None,
    description="Auto-generated summary information (call summary, locationOfIssue, etc.)"
)
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata extracted")


class SummaryRequest(BaseModel):
    """Model for summary requests"""
    sessionId: str = Field(..., description="Session identifier")


class SummaryResponse(BaseModel):
    """Model for summary responses — aligned with Summary model in form.model.py"""
    summary: str = Field(..., description="Conversation summary")
    locationOfIssue: Optional[LOCATION_OF_ISSUE] = Field(None, description="Extracted location of issue")
    actionTaken: Optional[ACTION_TAKEN] = Field(None, description="Suggested action taken")
    outcomeOfContact: Optional[OUTCOME_OF_CONTACT] = Field(None, description="Suggested outcome of contact")
    howDidYouKnowAboutOurLine: Optional[HOW_KNOWN] = Field(None, description="Extracted how they knew about the line")