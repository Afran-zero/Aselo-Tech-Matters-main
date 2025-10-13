import os
import json
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
from openai import AsyncOpenAI
from app.models.conversation_model import ChatMessage, AutoFillResponse
from app.utils.error_handler import LLMException
from app.utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

class LLMService:
    """Enhanced LLM service for child helpline - pure LLM approach without regex."""
    
    # Valid enums matching frontend TypeScript types
    VALID_PARISHES = {
        "Kingston", "St. Andrew", "St. Thomas", "St. Catherine", "Clarendon", 
        "Manchester", "St. Elizabeth", "Westmoreland", "Hanover", "St. James", 
        "Trelawny", "St. Ann", "St. Mary", "Portland", "Unknown"
    }
    
    VALID_GENDERS = {"Male", "Female", "Other", "Unknown"}
    
    VALID_LIVING_SITUATIONS = {
        "Alternative care", "Group residential facility", 
        "Homeless or marginally housed", "In detention",
        "Living independently", "With parent(s)", "With relatives", 
        "Other", "Unknown"
    }
    
    VALID_REGIONS = {"Unknown", "Cities", "Rural areas", "Town & semi-dense areas"}
    
    VALID_VULNERABLE_GROUPS = {
        "Child in conflict with the law", "Child living in conflict zone",
        "Child living in poverty", "Child member of an ethnic, racial or religious minority",
        "Child on the move (involuntarily)", "Child on the move (voluntarily)",
        "Child with disability", "LGBTQI+/SOGIESC child",
        "Out-of-school child", "Other"
    }

    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
        self.site_url = os.getenv("SITE_URL", "https://aselo-helpline.com")
        self.site_name = os.getenv("SITE_NAME", "Aselo Child Helpline")

        if not self.api_key:
            logger.warning("OPENROUTER_API_KEY not set. LLM requests will fail.")
            self.client = None
        else:
            self.client = AsyncOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
                timeout=90.0,
            )

    async def _make_request(
        self, 
        messages: List[dict], 
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 2000
    ) -> str:
        """Make a chat completion request to the LLM."""
        if not self.client:
            raise LLMException("LLM API key not configured", 500, "LLM_CONFIG_ERROR")

        api_messages = []
        if system_prompt:
            api_messages.append({"role": "system", "content": system_prompt})
        api_messages.extend(messages)

        try:
            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=api_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                timeout=60.0,
                extra_headers={
                    "HTTP-Referer": self.site_url, 
                    "X-Title": self.site_name
                }
            )

            if not completion.choices or not completion.choices[0].message:
                raise LLMException("No response from LLM", 500, "LLM_NO_RESPONSE")

            response_content = completion.choices[0].message.content
            logger.info(f"LLM response: {len(response_content)} chars")
            return response_content

        except Exception as e:
            logger.error(f"LLM API error: {str(e)}", exc_info=True)
            raise LLMException(f"LLM request failed: {str(e)}", 500, "LLM_API_ERROR")

    def _prepare_conversation_context(self, messages: List[ChatMessage]) -> str:
        """Prepare full conversation as formatted text."""
        lines = []
        for msg in messages:
            speaker = "COUNSELOR" if msg.sender == "assistant" else "CHILD"
            lines.append(f"{speaker}: {msg.message}")
        return "\n".join(lines)

    async def generate_chat_response(
        self, 
        messages: List[ChatMessage], 
        user_message: str
    ) -> str:
        """Generate empathetic counselor chat response."""
        system_prompt = (
    "You are a compassionate, professional child helpline counselor and intake assistant.\n\n"
    "Your mission:\n"
    "• Make the child feel safe, heard, and supported.\n"
    "• Gently collect information needed for their case form — without making it feel like an interrogation.\n"
    "• Ask one open, caring question at a time.\n"
    "• Use age-appropriate, simple, and warm language.\n"
    "• Validate their feelings and assure them that sharing helps you understand and support them better.\n"
    "• Always show empathy, but remain professional and calm.\n"
    "• Focus on safety, well-being, and comfort while gathering details.\n"
    "• Keep each response under 3–4 sentences.\n"
    "• Never rush — build trust gradually.\n"
    "• If the child mentions harm, abuse, or danger, acknowledge their courage and assess safety first.\n"
    "• Do not make promises you cannot keep.\n\n"
    "Your task is to ask about the following form details naturally, in the flow of conversation:\n"
    "— Child Information —\n"
    "1. First Name\n"
    "2. Last Name\n"
    "3. Gender\n"
    "4. Age\n"
    "5. Street Address\n"
    "6. Parish\n"
    "7. Phone #1\n"
    "8. Phone #2\n"
    "9. Nationality\n"
    "10. School Name\n"
    "11. Grade Level\n"
    "12. Living Situation (e.g., with parents, relatives, foster home)\n"
    "13. Vulnerable Groups (if applicable)\n"
    "14. Region\n\n"
    "— Category Information —\n"
    "15. Missing Children\n"
    "16. Violence\n"
    "17. Trafficking\n"
    "18. Mental Health\n"
    "19. Physical Health\n"
    "20. Accessibility\n"
    "21. Discrimination and Exclusion\n"
    "22. Family Relationships\n"
    "23. Peer Relationships\n"
    "24. Education and Occupation\n"
    "25. Sexuality\n"
    "26. Disability\n"
    "27. Non-Counselling Contacts\n\n"
    "Approach:\n"
    "Start by building trust and comfort. Then, gradually ask for these details when appropriate, using gentle, human-centered questions. "
    "Avoid sounding like a form or checklist — your tone should feel natural, conversational, and kind."
)



        conversation_text = self._prepare_conversation_context(messages)
        
        api_messages = [
            {"role": "user", "content": f"CONVERSATION SO FAR:\n{conversation_text}\n\nCHILD'S NEW MESSAGE:\n{user_message}"}
        ]

        response = await self._make_request(
            api_messages, 
            system_prompt,
            temperature=0.8,
            max_tokens=400
        )
        return response.strip()

    def _clean_json_response(self, raw_response: str) -> str:
        """Extract JSON from LLM response using pure string operations."""
        # Remove whitespace
        cleaned = raw_response.strip()
        
        # Find first { and last }
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_str = cleaned[start_idx:end_idx + 1]
            return json_str
        
        # If no valid JSON found, return empty object
        return "{}"

    def _validate_enum_field(self, value: Optional[str], valid_set: set) -> Optional[str]:
        """Validate a field against valid enum values."""
        if not value:
            return None
        
        # Direct match
        if value in valid_set:
            return value
        
        # Case-insensitive match
        value_lower = value.lower()
        for valid in valid_set:
            if value_lower == valid.lower():
                return valid
        
        return None

    def _normalize_age(self, age: Any) -> Optional[str]:
        """Normalize age using LLM intelligence."""
        if not age:
            return None
        
        age_str = str(age).strip()
        
        # Let LLM handle age normalization
        return age_str

    def _validate_child_data(self, child: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and normalize all child fields."""
        validated = {}
        
        # Simple string fields
        for field in ["firstName", "lastName", "streetAddress", "phone1", "phone2", 
                      "nationality", "schoolName", "gradeLevel"]:
            if field in child and child[field]:
                validated[field] = str(child[field]).strip()
        
        # Enum validations
        validated["gender"] = self._validate_enum_field(child.get("gender"), self.VALID_GENDERS)
        validated["parish"] = self._validate_enum_field(child.get("parish"), self.VALID_PARISHES)
        validated["livingSituation"] = self._validate_enum_field(
            child.get("livingSituation"), self.VALID_LIVING_SITUATIONS
        )
        validated["region"] = self._validate_enum_field(child.get("region"), self.VALID_REGIONS)
        
        # Age
        validated["age"] = self._normalize_age(child.get("age"))
        
        # Vulnerable groups validation
        if "vulnerableGroups" in child and isinstance(child["vulnerableGroups"], list):
            validated["vulnerableGroups"] = [
                vg for vg in child["vulnerableGroups"] 
                if vg in self.VALID_VULNERABLE_GROUPS
            ]
            if not validated["vulnerableGroups"]:
                validated["vulnerableGroups"] = None
        
        # Remove None values
        return {k: v for k, v in validated.items() if v is not None}

    def _apply_intelligent_defaults(self, child: Dict[str, Any]) -> Dict[str, Any]:
        """Apply context-aware defaults based on available data."""
        # Infer nationality from Jamaican parish
        if not child.get("nationality") and child.get("parish"):
            if child["parish"] in self.VALID_PARISHES and child["parish"] != "Unknown":
                child["nationality"] = "Jamaican(Assumed)"
                logger.info("Inferred nationality: Jamaican ")
        
        # Infer region from parish
        if not child.get("region") and child.get("parish"):
            parish = child["parish"]
            if parish in {"Kingston", "St. Andrew"}:
                child["region"] = "Cities"
            elif parish in {"Portland", "St. Mary", "St. Elizabeth"}:
                child["region"] = "Rural areas"
            elif parish in self.VALID_PARISHES and parish != "Unknown":
                child["region"] = "Town & semi-dense areas"
            if child.get("region"):
                logger.info(f"Inferred region from parish: {child['region']}")
        
        return child
    


    async def extract_form_data(self, messages: List[ChatMessage]) -> AutoFillResponse:
        """Extract comprehensive form data using pure LLM intelligence."""
        conversation_text = self._prepare_conversation_context(messages)
        
        system_prompt = self._build_extraction_prompt()
        
        api_messages = [{
            "role": "user",
            "content": (
                f"CONVERSATION:\n{conversation_text}\n\n"
                "Extract ALL information mentioned into structured JSON format. "
                "Be thorough and extract everything stated, but never invent or assume information."
            )
        }]

        try:
            raw_response = await self._make_request(
                api_messages, 
                system_prompt,
                temperature=0.1,
                max_tokens=3000
            )
            
            logger.info(f"Extraction raw response length: {len(raw_response)}")
            
            # Parse JSON
            json_str = self._clean_json_response(raw_response)
            data = json.loads(json_str)
            logger.debug(f"Raw parsed LLM JSON data:\n{json.dumps(data, indent=2)}")
            
            # Extract and validate sections
            child = self._validate_child_data(data.get("child", {}))
            child = self._apply_intelligent_defaults(child)
            
            # With this:
            summary = data.get("summary", {})
            raw_category = data.get("category", {})

# Normalize all expected category keys to be lists (never None)
            CATEGORY_KEYS = [
              "violence", "mental_health", "family_relationships",
                 "education_and_occupation", "peer_relationships",
                     "missing_children", "trafficking", "physical_health",
                         "accessibility", "discrimination_and_exclusion",
                           "sexuality", "disability", "non_counselling_contacts"
                            ]

            category = {}
            for key in CATEGORY_KEYS:
              val = raw_category.get(key)
              if isinstance(val, list):
        # Keep only non-empty strings
               category[key] = [str(item).strip() for item in val if isinstance(item, str) and item.strip()]
              else:
                   category[key] = []  # Default to empty list, not None
            
            # Ensure required fields have defaults
            if not summary.get("callSummary"):
                summary["callSummary"] = "Conversation in progress."
            if summary.get("keepConfidential") is None:
                summary["keepConfidential"] = True
            
            # Build response
            response = AutoFillResponse(
                firstName=child.get("firstName"),
                lastName=child.get("lastName"),
                gender=child.get("gender"),
                age=child.get("age"),
                streetAddress=child.get("streetAddress"),
                parish=child.get("parish"),
                phone1=child.get("phone1"),
                phone2=child.get("phone2"),
                nationality=child.get("nationality"),
                schoolName=child.get("schoolName"),
                gradeLevel=child.get("gradeLevel"),
                livingSituation=child.get("livingSituation"),
                vulnerableGroups=child.get("vulnerableGroups"),
                region=child.get("region"),
                suggested_categories=category if isinstance(category, dict) else {},
                summary=summary ,
                metadata=data.get("metadata", {})
            )
            
            logger.info(f"Successfully extracted form data")
            return response

        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}", exc_info=True)
            return AutoFillResponse(summary={"callSummary": "Unable to auto-fill. Please enter manually."})

        except Exception as e:
            logger.error(f"Extraction failed: {e}", exc_info=True)
            return AutoFillResponse(summary={"callSummary": "Unable to auto-fill. Please enter manually."})


    def _build_extraction_prompt(self) -> str:
        """Build comprehensive extraction prompt with detailed instructions."""
        parishes_list = ', '.join(sorted(self.VALID_PARISHES))
        genders_list = ', '.join(sorted(self.VALID_GENDERS))
        living_situations_list = ', '.join(sorted(self.VALID_LIVING_SITUATIONS))
        regions_list = ', '.join(sorted(self.VALID_REGIONS))
        vulnerable_groups_list = ', '.join(sorted(list(self.VALID_VULNERABLE_GROUPS)))
        
        return f"""You are an expert data extraction assistant for a child helpline system in Jamaica.

TASK: Extract ALL explicitly mentioned information from the conversation into structured JSON.

OUTPUT FORMAT - You MUST output valid JSON with this exact structure:
{{
  "child": {{
    "firstName": "string or null",
    "lastName": "string or null",
    "gender": "{genders_list} assume gender though name if not stated OR 'Unknown' OR null",
    "age": "format as 2 digits like 01, 05, 14 OR 'Unborn' OR '>25' OR 'Unknown' OR null",
    "streetAddress": "string or null",
    "parish": "{parishes_list}",
    "phone1": "string or null",
    "phone2": "string or null",
    "nationality": "string or null",
    "schoolName": "string or null",
    "gradeLevel": "string or null",
    "livingSituation": "{living_situations_list} CRITICAL - LIVING SITUATION RULES:You MUST use EXACTLY one of these values - NEVER invent new values or use synonyms
- "Extended family placement" → USE "With relatives"
- "Foster care" → USE "Alternative care" 
- "Living with grandparents/aunts/uncles" → USE "With relatives"
- If it doesn't match exactly, use "Other" or "Unknown"
    "vulnerableGroups": ["array of strings from valid set"],
    "region": "{regions_list}"
  }},
  "category": { {
    "missing_children": [
      "Child abduction",
      "Lost, unaccounted for or otherwise missing child",
      "Runaway",
      "Unspecified/Other"
    ],
    "violence": [
      "Bullying in school",
      "Bullying out of school",
      "Child labour (general)",
      "Child labour (domestic)",
      "Cyberbullying",
      "Emotional maltreatment/abuse",
      "Exposure to criminal violence",
      "Exposure to domestic violence",
      "Exposure to pornography",
      "Gender-based harmful traditional practices (other than FGM)",
      "Harmful traditional practices other than child marriage and FGM",
      "Inappropriate sex talk",
      "Indecent assault",
      "Neglect (emotional)",
      "Neglect (education)",
      "Neglect (health & nutrition)",
      "Neglect (physical)",
      "Neglect (or negligent treatment)",
      "Online child sexual abuse and exploitation",
      "Physical maltreatment/abuse",
      "Sexual violence",
      "Verbal maltreatment/abuse",
      "Unspecified/Other"
    ],
    "trafficking": [
      "Child begging",
      "Child used for criminal activity",
      "Commercial sexual exploitation (offline)",
      "Commercial sexual exploitation (online)",
      "Labour exploitation (domestic servitude)"
    ],
    "mental_health": [
      "Addictive behaviours and substance use",
      "Behavioural problems",
      "Concerns about the self",
      "Emotional distress - anger problems",
      "Emotional distress - fear and anxiety problems",
      "Emotional distress - mood problems",
      "Hyperactivity/attention deficit",
      "Neurodevelopmental concerns",
      "Problems with eating behaviour",
      "Self-esteem issues",
      "Self-harming behaviour",
      "Sleep disorders",
      "Stress",
      "Suicidal thoughts and suicide attempts",
      "Traumatic distress",
      "Wellbeing support",
      "Unspecified/Other"
    ],
    "physical_health": [
      "COVID-19",
      "General medical or lifestyle concerns",
      "Medical or lifestyle information about HIV/AIDS",
      "Pregnancy and maternal care",
      "Sexual and reproductive health",
      "Nutrition",
      "Unspecified/Other"
    ],
    "accessibility": [
      "Career Guidance",
      "Education",
      "Essential needs (food, shelter, water, clothing)",
      "Financial services",
      "General healthcare services",
      "Legal services and advice",
      "Mental health services",
      "Sexual health services",
      "Socio-economical services",
      "Unspecified/Other"
    ],
    "discrimination_and_exclusion": [
      "Ethnicity/nationality",
      "Financial situation",
      "Gender",
      "Gender identity or expression and sexual orientation",
      "Health",
      "Philosophical or religious beliefs",
      "Socio-economic situation",
      "Street children",
      "Unspecified/Other"
    ],
    "family_relationships": [
      "Adoption, fostering, and extended family placement",
      "Child in children's home",
      "Divorce/separation of parents",
      "Family health and wellbeing",
      "Family problems/disputes - conflict between parents/caregivers",
      "Family problems/disputes - conflict between parents/caregivers and child",
      "Family problems/disputes - conflict between child and other members of the family",
      "General family issues",
      "Grief/bereavement - family",
      "Left behind children",
      "Mental health - parental/relative",
      "Relationship with sibling(s)",
      "Relationship to caregiver"
    ],
    "peer_relationships": [
      "Friends and friendships",
      "Grief/bereavement - peers",
      "Partner relationships",
      "Classmates/colleagues relationships",
      "Unspecified/Other"
    ],
    "education_and_occupation": [
      "Academic issues",
      "Challenges with online schooling",
      "Child not attending school",
      "Child truanting from school",
      "Corporal punishment",
      "Homework/study tips",
      "Learning problems",
      "Performance anxiety",
      "Problems at work",
      "Teacher and school problems",
      "Unspecified/Other"
    ],
    "sexuality": [
      "Sexual orientation and gender identity",
      "Sexual behaviours",
      "Unspecified/Other"
    ],
    "disability": [
      "Intellectual disability",
      "Hearing disability",
      "Physical disability",
      "Visual disability"
    ],
    "non_counselling_contacts": [
      "Complaints about the child helpline",
      "Questions about the child helpline",
      "Questions about other services",
      "\"Thank you for your assistance\"",
      "Unspecified/Other"
    ]
  }},
  "summary": {{
    "callSummary": "Brief 2-3 sentence summary of main issue and context",
    "keepConfidential": true,
    "locationOfIssue": "'Unknown' | 'Home (own)' | 'Home (other)' | 'Educational Establishment' | 'Institution' | 'Online' | 'Public place' | 'Other'",
    "actionTaken": [
      Direct interventions by the child helpline' | 'Provision of information about SafeSpot' | 'Recommendations of resources' | 'Recommendation that young person contact SafeSpot' | 'Referrals to child protection agencies' | 'Referrals to law enforcement agencies' | 'Referrals to general healthcare professionals' | 'Referrals to mental health services' | 'Referrals to other organisations' | 'Referrals to school counsellors' | 'Reports to Child Sexual Abuse Material (CSAM) platform' | 'None' | 'Other'
    ],


    "outcomeOfContact": "Resolved OR Follow up by next shift OR Follow up with external entity OR null",
    "repeatCaller": true/false/null,
    "okForCaseWorkerToCall": true/false/null,
    "didTheChildFeelWeSolvedTheirProblem": true/false/null,
    "wouldTheChildRecommendUsToAFriend": true/false/null,
    "didYouDiscussRightsWithTheChild": true/false/null
  }},
  "metadata": {{}}
}}

VALID VULNERABLE GROUPS:
{vulnerable_groups_list}

EXTRACTION RULES:
1. Extract ONLY information explicitly stated in the conversation
2. Use null for any field not clearly mentioned - DO NOT GUESS
3. Match enum values EXACTLY (case-sensitive)
4. For age: if mentioned as number, format as 2 digits (1 becomes "01", 5 becomes "05", 14 becomes "14")
5. Be conservative - when uncertain, use null
6. Categories: only include categories where specific issues are discussed
7. CallSummary: always provide a brief factual summary of the conversation
8. For boolean fields: use true, false, or null (not strings like "true")
9. Parish must be exact match from valid list
10. Living situation must be exact match from valid list

CATEGORY KEYS (only include if relevant issues discussed):
- missing_children: issues about lost, runaway, or abducted children
- violence: bullying, abuse, neglect, maltreatment
- trafficking: exploitation, forced labor
- mental_health: stress, anxiety, depression, self-harm, behavioral issues
- physical_health: medical concerns, pregnancy, nutrition, HIV/AIDS
- accessibility: services needed (education, healthcare, legal)
- discrimination_and_exclusion: discrimination based on any factor
- family_relationships: family conflicts, divorce, grief, caregiver issues
- peer_relationships: friends, classmates, partner relationships
- education_and_occupation: school problems, learning issues, work problems
- sexuality: sexual orientation, behaviors
- disability: physical, intellectual, hearing, visual disabilities
- non_counselling_contacts: questions about helpline, thank you messages

AGE FORMATTING EXAMPLES:
- If child says "I am 7" or "7 years old" -> "07"
- If child says "I'm 14" -> "14"
- If child says "my baby" or "not born yet" -> "Unborn"
- If age unknown -> "Unknown"
- If over 25 -> ">25"

CRITICAL REQUIREMENTS:
- Output ONLY valid JSON
- No markdown formatting, no code blocks, no explanations
- Start directly with {{ and end with }}
- Use double quotes for strings
- Use null (not "null" or "None") for missing values
- Use true/false (not "true"/"false") for booleans
- Ensure all opening braces {{ have closing braces }}
- Ensure all opening brackets [ have closing brackets ]

ANALYSIS APPROACH:
1. Read the ENTIRE conversation carefully
2. Identify what information is explicitly stated
3. Match stated information to the correct fields
4. Format according to requirements
5. Use null for anything not explicitly mentioned
6. Double-check JSON syntax before responding"""

    async def generate_summary(self, messages: List[ChatMessage]) -> str:
        """Generate professional case summary for records."""
        conversation_text = self._prepare_conversation_context(messages)
        
        system_prompt = (
            "You are a professional child helpline case worker writing case summaries.\n\n"
            "Create a concise, factual summary including:\n"
            "• Main issue/concern raised by the child\n"
            "• Child's demographics (age, gender, location if known)\n"
            "• Key vulnerabilities or risk factors identified\n"
            "• Child's expressed needs or requests\n"
            "• Any immediate safety concerns\n"
            "• Actions taken or recommended by counselor\n\n"
            "Requirements:\n"
            "- Write 3-5 sentences maximum\n"
            "- Use professional, empathetic tone\n"
            "- State only facts from the conversation\n"
            "- Do not speculate or make assumptions\n"
            "- Maintain child's dignity and privacy\n"
            "- Suitable for case records and handover to other staff\n"
            "- Use third person perspective\n\n"
            "Example format:\n"
            "A 14-year-old female from Kingston contacted the helpline regarding bullying at school. "
            "She reported feeling anxious and isolated. The counselor provided emotional support and "
            "discussed coping strategies. Referral to school counselor recommended."
        )
        
        api_messages = [{
            "role": "user",
            "content": f"Conversation:\n{conversation_text}\n\nWrite a professional case summary for our records."
        }]

        try:
            summary = await self._make_request(
                api_messages, 
                system_prompt,
                temperature=0.3,
                max_tokens=600
            )
            return summary.strip()
        except Exception as e:
            logger.error(f"Summary generation failed: {e}", exc_info=True)
            return "Unable to generate summary. Please review conversation manually."

    async def analyze_conversation_quality(self, messages: List[ChatMessage]) -> Dict[str, Any]:
        """Analyze conversation quality and provide insights for counselor improvement."""
        conversation_text = self._prepare_conversation_context(messages)
        
        system_prompt = (
            "You are a supervisor evaluating a child helpline conversation.\n\n"
            "Analyze the conversation and provide structured feedback as JSON:\n"
            "{\n"
            '  "empathy_score": 1-10,\n'
            '  "information_gathered": 1-10,\n'
            '  "safety_assessment": 1-10,\n'
            '  "strengths": ["list of positive aspects"],\n'
            '  "improvements": ["list of areas for improvement"],\n'
            '  "urgent_concerns": ["any immediate safety issues identified"],\n'
            '  "overall_assessment": "brief summary"\n'
            "}\n\n"
            "Focus on:\n"
            "- How well counselor showed empathy and active listening\n"
            "- Effectiveness of information gathering\n"
            "- Safety assessment and risk identification\n"
            "- Appropriate use of language\n"
            "- Building trust and rapport"
        )
        
        api_messages = [{
            "role": "user",
            "content": f"Analyze this conversation:\n{conversation_text}"
        }]

        try:
            response = await self._make_request(
                api_messages,
                system_prompt,
                temperature=0.2,
                max_tokens=800
            )
            json_str = self._clean_json_response(response)
            return json.loads(json_str)
        except Exception as e:
            logger.error(f"Quality analysis failed: {e}", exc_info=True)
            return {
                "error": "Analysis unavailable",
                "overall_assessment": "Unable to analyze conversation quality"
            }


# Singleton instance
llm_service = LLMService()