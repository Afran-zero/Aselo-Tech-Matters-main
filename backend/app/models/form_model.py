from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Literal
from datetime import datetime, timezone


class Child(BaseModel):
    """Model for child data"""
    firstName: str = Field(..., description="First Name", examples=["Maria"])
    lastName: Optional[str] = Field(None, description="Last Name", examples=["Rodriguez"])
    gender: Optional[Literal["Male", "Female", "Other", "Unknown"]] = Field(None, description="Gender")
    age: Optional[Literal[
        "Unborn", "0", "01", "02", "03", "04", "05", "06", "07", "08", "09",
        "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
        "21", "22", "23", "24", "25", ">25", "Unknown"
    ]] = Field(None, description="Age")
    streetAddress: Optional[str] = Field(None, description="Street Address")
    parish: Optional[Literal[
        "Kingston", "St. Andrew", "St. Thomas", "St. Catherine", "Clarendon", "Manchester",
        "St. Elizabeth", "Westmoreland", "Hanover", "St. James", "Trelawny", "St. Ann",
        "St. Mary", "Portland", "Unknown"
    ]] = Field(None, description="Parish")
    phone1: Optional[str] = Field(None, description="Phone #1")
    phone2: Optional[str] = Field(None, description="Phone #2")
    nationality: Optional[str] = Field(None, description="Nationality")
    schoolName: Optional[str] = Field(None, description="School Name")
    gradeLevel: Optional[str] = Field(None, description="Grade Level")
    livingSituation: Optional[Literal[
        "Alternative care", "Group residential facility", "Homeless or marginally housed",
        "In detention", "Living independently", "With parent(s)", "With relatives", "Other", "Unknown"
    ]] = Field(None, description="Living Situation")
    vulnerableGroups: Optional[List[Literal[
        "Child in conflict with the law", "Child living in conflict zone", "Child living in poverty",
        "Child member of an ethnic, racial or religious minority", "Child on the move (involuntarily)",
        "Child on the move (voluntarily)", "Child with disability", "LGBTQI+/SOGIESC child",
        "Out-of-school child", "Other"
    ]]] = Field(None, description="Vulnerable Groups")
    region: Optional[Literal["Unknown", "Cities", "Rural areas", "Town & semi-dense areas"]] = Field(None, description="Region")


class Category(BaseModel):
    """Model for category data"""
    missing_children: Optional[List[Literal[
        "Child abduction", "Lost, unaccounted for or otherwise missing child", "Runaway", "Unspecified/Other"
    ]]] = Field(None, alias="Missing children", description="Missing children subcategories")
    
    violence: Optional[List[Literal[
        "Bullying in school", "Bullying out of school", "Child labour (general)", "Child labour (domestic)",
        "Cyberbullying", "Emotional maltreatment/abuse", "Exposure to criminal violence",
        "Exposure to domestic violence", "Exposure to pornography",
        "Gender-based harmful traditional practices (other than FGM)",
        "Harmful traditional practices other than child marriage and FGM", "Inappropriate sex talk",
        "Indecent assault", "Neglect (emotional)", "Neglect (education)", "Neglect (health & nutrition)",
        "Neglect (physical)", "Neglect (or negligent treatment)", "Online child sexual abuse and exploitation",
        "Physical maltreatment/abuse", "Sexual violence", "Verbal maltreatment/abuse", "Unspecified/Other"
    ]]] = Field(None, alias="Violence", description="Violence subcategories")
    
    trafficking: Optional[List[Literal[
        "Child begging", "Child used for criminal activity", "Commercial sexual exploitation (offline)",
        "Commercial sexual exploitation (online)", "Labour exploitation (domestic servitude)"
    ]]] = Field(None, alias="Trafficking", description="Trafficking subcategories")
    
    mental_health: Optional[List[Literal[
        "Addictive behaviours and substance use", "Behavioural problems", "Concerns about the self",
        "Emotional distress - anger problems", "Emotional distress - fear and anxiety problems",
        "Emotional distress - mood problems", "Hyperactivity/attention deficit", "Neurodevelopmental concerns",
        "Problems with eating behaviour", "Self-esteem issues", "Self-harming behaviour", "Sleep disorders",
        "Stress", "Suicidal thoughts and suicide attempts", "Traumatic distress", "Wellbeing support", "Unspecified/Other"
    ]]] = Field(None, alias="Mental Health", description="Mental Health subcategories")
    
    physical_health: Optional[List[Literal[
        "COVID-19", "General medical or lifestyle concerns", "Medical or lifestyle information about HIV/AIDS",
        "Pregnancy and maternal care", "Sexual and reproductive health", "Nutrition", "Unspecified/Other"
    ]]] = Field(None, alias="Physical Health", description="Physical Health subcategories")
    
    accessibility: Optional[List[Literal[
        "Career Guidance", "Education", "Essential needs (food, shelter, water, clothing)", "Financial services",
        "General healthcare services", "Legal services and advice", "Mental health services",
        "Sexual health services", "Socio-economical services", "Unspecified/Other"
    ]]] = Field(None, alias="Accessibility", description="Accessibility subcategories")
    
    discrimination_and_exclusion: Optional[List[Literal[
        "Ethnicity/nationality", "Financial situation", "Gender", "Gender identity or expression and sexual orientation",
        "Health", "Philosophical or religious beliefs", "Socio-economic situation", "Street children", "Unspecified/Other"
    ]]] = Field(None, alias="Discrimination and Exclusion", description="Discrimination and Exclusion subcategories")
    
    family_relationships: Optional[List[Literal[
        "Adoption, fostering, and extended family placement", "Child in children's home", "Divorce/separation of parents",
        "Family health and wellbeing", "Family problems/disputes - conflict between parents/caregivers",
        "Family problems/disputes - conflict between parents/caregivers and child",
        "Family problems/disputes - conflict between child and other members of the family",
        "General family issues", "Grief/bereavement - family", "Left behind children",
        "Mental health - parental/relative", "Relationship with sibling(s)", "Relationship to caregiver"
    ]]] = Field(None, alias="Family Relationships", description="Family Relationships subcategories")
    
    peer_relationships: Optional[List[Literal[
        "Friends and friendships", "Grief/bereavement - peers", "Partner relationships",
        "Classmates/colleagues relationships", "Unspecified/Other"
    ]]] = Field(None, alias="Peer Relationships", description="Peer Relationships subcategories")
    
    education_and_occupation: Optional[List[Literal[
        "Academic issues", "Challenges with online schooling", "Child not attending school", "Child truanting from school",
        "Corporal punishment", "Homework/study tips", "Learning problems", "Performance anxiety", "Problems at work",
        "Teacher and school problems", "Unspecified/Other"
    ]]] = Field(None, alias="Education and Occupation", description="Education and Occupation subcategories")
    
    sexuality: Optional[List[Literal[
        "Sexual orientation and gender identity", "Sexual behaviours", "Unspecified/Other"
    ]]] = Field(None, alias="Sexuality", description="Sexuality subcategories")
    
    disability: Optional[List[Literal[
        "Intellectual disability", "Hearing disability", "Physical disability", "Visual disability"
    ]]] = Field(None, alias="Disability", description="Disability subcategories")
    
    non_counselling_contacts: Optional[List[Literal[
        "Complaints about the child helpline", "Questions about the child helpline",
        "Questions about other services", "\"Thank you for your assistance\"", "Unspecified/Other"
    ]]] = Field(None, alias="Non-Counselling contacts", description="Non-Counselling contacts subcategories")


class Summary(BaseModel):
    """Model for summary data"""
    callSummary: str = Field(..., description="Contact Summary", examples=["Child reported bullying at school."])
    summaryAccuracy: Optional[Literal["Unknown", "Very accurate", "Somewhat accurate", "Not accurate"]] = Field(None, description="Summary Accuracy")
    summaryFeedback: Optional[str] = Field(None, description="Summary Feedback")
    locationOfIssue: Optional[Literal[
        "Unknown", "Home (own)", "Home (other)", "Educational Establishment", "Institution",
        "Online", "Public place", "Other"
    ]] = Field(None, description="Location of Issue")
    otherLocation: Optional[str] = Field(None, description="Other Location")
    actionTaken: Optional[Literal[
        "Direct interventions by the child helpline", "Provision of information about SafeSpot",
        "Recommendations of resources", "Recommendation that young person contact SafeSpot",
        "Referrals to child protection agencies", "Referrals to law enforcement agencies",
        "Referrals to general healthcare professionals", "Referrals to mental health services",
        "Referrals to other organisations", "Referrals to school counsellors",
        "Reports to Child Sexual Abuse Material"
    ]] = Field(None, description="Action Taken")
    outcomeOfContact: Optional[Literal["Resolved", "Follow up by next shift", "Follow up with external entity"]] = Field(None, description="Outcome of Contact")
    howDidYouKnowAboutOurLine: Optional[Literal[
        "AI", "Advertisement", "Social media", "SMS/Text Message", "Traditional Media", "Word of Mouth"
    ]] = Field(None, description="How Did You Know About Our Line")
    repeatCaller: Optional[bool] = Field(None, description="Repeat Caller")
    keepConfidential: bool = Field(True, description="Keep Confidential")
    okForCaseWorkerToCall: Optional[bool] = Field(None, description="Ok For Case Worker To Call")
    didTheChildFeelWeSolvedTheirProblem: Optional[bool] = Field(None, description="Did The Child Feel We Solved Their Problem")
    wouldTheChildRecommendUsToAFriend: Optional[bool] = Field(None, description="Would The Child Recommend Us To A Friend")
    didYouDiscussRightsWithTheChild: Optional[bool] = Field(None, description="Did You Discuss Rights With The Child")


class FormData(BaseModel):
    """Model for form data"""
    child: Child = Field(..., description="Child data")
    category: Category = Field(..., description="Category data")
    summary: Summary = Field(..., description="Summary data")
    additional_fields: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional form fields")


class FormSubmissionRequest(BaseModel):
    """Model for form submission requests"""
    sessionId: str = Field(..., description="Session identifier", examples=["sess_abc123xyz"])
    formData: FormData = Field(..., description="Form data to submit")


class FormSubmissionResponse(BaseModel):
    """Model for form submission responses"""
    success: bool = Field(..., description="Submission success status")
    message: str = Field(..., description="Confirmation message")
    submissionId: str = Field(..., description="Unique submission identifier", examples=["subm_def456uvw"])


class FormSubmission(BaseModel):
    """Model for stored form submissions"""
    sessionId: str = Field(..., description="Session identifier")
    submissionId: str = Field(..., description="Unique submission identifier")
    formData: FormData = Field(..., description="Submitted form data")
    submitted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Submission timestamp (UTC)")
    status: str = Field(default="submitted", description="Submission status")


# Simplified version of form_model.py for a different form structure


"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class FormData(BaseModel):
   #Model for form data
    name: Optional[str] = Field(None, description="User name")
    email: Optional[str] = Field(None, description="User email")
    phone: Optional[str] = Field(None, description="User phone number")
    address: Optional[str] = Field(None, description="User address")
    notes: Optional[str] = Field(None, description="Additional notes")
    # Allow for additional fields that might be added later
    additional_fields: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional form fields")


class FormSubmissionRequest(BaseModel):
    #Model for form submission requests
    sessionId: str = Field(..., description="Session identifier")
    formData: FormData = Field(..., description="Form data to submit")


class FormSubmissionResponse(BaseModel):
    #Model for form submission responses
    success: bool = Field(..., description="Submission success status")
    message: str = Field(..., description="Confirmation message")
    submissionId: str = Field(..., description="Unique submission identifier")


class FormSubmission(BaseModel):
   #Model for stored form submissions
    sessionId: str = Field(..., description="Session identifier")
    submissionId: str = Field(..., description="Unique submission identifier")
    formData: FormData = Field(..., description="Submitted form data")
    submitted_at: datetime = Field(default_factory=datetime.now, description="Submission timestamp")
    status: str = Field(default="submitted", description="Submission status")

    """