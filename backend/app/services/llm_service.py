import os
import json
import re
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
from openai import AsyncOpenAI
from app.models.conversation_model import ChatMessage, AutoFillResponse
from app.utils.error_handler import LLMException
from app.utils.logger import get_logger

# Load environment variables
load_dotenv()

logger = get_logger(__name__)

class LLMService:
    """Service for handling LLM-based operations for child helpline conversations."""
    
    # Constants
    VALID_PARISHES = {
        "Kingston", "St. Andrew", "St. Thomas", "St. Catherine", "Clarendon", 
        "Manchester", "St. Elizabeth", "Westmoreland", "Hanover", "St. James", 
        "Trelawny", "St. Ann", "St. Mary", "Portland"
    }
    
    VALID_VULNERABLE_GROUPS = {
        "Child in conflict with the law",
        "Child living in conflict zone",
        "Child living in poverty",
        "Child member of an ethnic, racial or religious minority",
        "Child on the move (involuntarily)",
        "Child on the move (voluntarily)",
        "Child with disability",
        "LGBTQI+/SOGIESC child",
        "Out-of-school child",
        "Other"
    }
    
    VALID_REGIONS = {"Cities", "Rural areas", "Town & semi-dense areas"}
    
    # Pydantic model expects these exact values
    VALID_LIVING_SITUATIONS = {
        "Alternative care",
        "Group residential facility", 
        "Homeless or marginally housed",
        "In detention",
        "Living independently",
        "With parent(s)",
        "With relatives",
        "Other",
        "Unknown"
    }
    
    # Mapping for LLM output to Pydantic enum
    LIVING_SITUATION_MAPPING = {
        "with parents": "With parent(s)",
        "with parent": "With parent(s)",
        "lives with parents": "With parent(s)",
        "with mother": "With parent(s)",
        "with father": "With parent(s)",
        "with mom": "With parent(s)",
        "with dad": "With parent(s)",
        "with me and my husband": "With parent(s)",
        "with us": "With parent(s)",
        "with relatives": "With relatives",
        "with family": "With relatives",
        "with aunt": "With relatives",
        "with uncle": "With relatives",
        "with grandparents": "With relatives",
        "with grandmother": "With relatives",
        "with grandfather": "With relatives",
        "with guardian": "Alternative care",
        "foster care": "Alternative care",
        "in foster care": "Alternative care",
        "group home": "Group residential facility",
        "residential facility": "Group residential facility",
        "institution": "Group residential facility",
        "homeless": "Homeless or marginally housed",
        "on the streets": "Homeless or marginally housed",
        "detention": "In detention",
        "jail": "In detention",
        "alone": "Living independently",
        "by myself": "Living independently",
        "independently": "Living independently",
        "other": "Other",
        "unknown": "Unknown"
    }

    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "nvidia/nemotron-nano-9b-v2:free")
        self.site_url = os.getenv("SITE_URL", "https://your-site-url.com")
        self.site_name = os.getenv("SITE_NAME", "Aselo Backend")

        if not self.api_key:
            logger.warning("OPENROUTER_API_KEY not set. LLM requests will fail.")
            self.client = None
        else:
            self.client = AsyncOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
                timeout=60.0,
            )

    async def _make_request(
        self, 
        messages: List[dict], 
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 1500
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
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                timeout=30.0,
                extra_headers={
                    "HTTP-Referer": self.site_url, 
                    "X-Title": self.site_name
                }
            )

            if not completion.choices or not completion.choices[0].message:
                raise LLMException("No response from LLM", 500, "LLM_NO_RESPONSE")

            response_content = completion.choices[0].message.content
            logger.info(f"LLM response received: {len(response_content)} characters")
            return response_content

        except LLMException:
            raise
        except Exception as e:
            logger.error(f"LLM API error: {str(e)}", exc_info=True)
            raise LLMException(f"LLM request failed: {str(e)}", 500, "LLM_API_ERROR")

    def _prepare_conversation_context(self, messages: List[ChatMessage]) -> List[dict]:
        """Prepare messages for API format."""
        api_messages = []
        for msg in messages:
            role = "user" if msg.sender == "user" else "assistant"
            api_messages.append({"role": role, "content": msg.message})
        return api_messages

    async def generate_chat_response(
        self, 
        messages: List[ChatMessage], 
        user_message: str
    ) -> str:
        """Generate counselor-style chat response."""
        system_prompt = (
            "You are a compassionate, professional child helpline counselor for Aselo. "
            "Your role is to:\n"
            "1. Listen actively and validate the child's feelings\n"
            "2. Gently gather information to understand their situation\n"
            "3. Ask clear, open-ended questions one at a time\n"
            "4. Build trust gradually—never rush or overwhelm\n"
            "5. Focus on immediate safety, well-being, and needs\n"
            "6. Use age-appropriate, simple language\n"
            "7. Maintain confidentiality unless there's risk of serious harm\n"
            "8. Never make promises you cannot keep\n"
            "9. Be empathetic but professional\n\n"
            "If the child expresses thoughts of self-harm or mentions abuse, "
            "acknowledge their courage in sharing and gently ask if they are safe right now."
        )

        api_messages = self._prepare_conversation_context(messages)
        api_messages.append({"role": "user", "content": user_message})

        try:
            response = await self._make_request(
                api_messages, 
                system_prompt,
                temperature=0.7,
                max_tokens=500
            )
            return response
        except Exception as e:
            logger.error(f"Failed to generate chat response: {str(e)}")
            raise LLMException(f"Failed to generate chat response: {str(e)}")

    def _clean_json_response(self, raw_response: str) -> str:
        """Clean and extract JSON from LLM response."""
        json_str = re.sub(r"^```(?:json)?\s*", "", raw_response)
        json_str = re.sub(r"\s*```$", "", json_str).strip()

        if not json_str.startswith("{"):
            match = re.search(r"\{.*\}", json_str, re.DOTALL)
            json_str = match.group(0) if match else "{}"
        
        return json_str

    def _normalize_living_situation(self, living_situation: Optional[str]) -> Optional[str]:
        """Normalize living situation to match Pydantic enum values."""
        if not living_situation:
            return None
        
        ls_lower = living_situation.lower().strip()
        
        # Direct match
        if living_situation in self.VALID_LIVING_SITUATIONS:
            return living_situation
        
        # Try exact mapping
        if ls_lower in self.LIVING_SITUATION_MAPPING:
            normalized = self.LIVING_SITUATION_MAPPING[ls_lower]
            logger.info(f"Normalized living situation: '{living_situation}' -> '{normalized}'")
            return normalized
        
        # Partial match - contains key phrases
        for key, value in self.LIVING_SITUATION_MAPPING.items():
            if key in ls_lower:
                logger.info(f"Normalized living situation: '{living_situation}' -> '{value}' (partial match)")
                return value
        
        # Default to "Other" if we can't match
        logger.warning(f"Could not normalize living situation: '{living_situation}', defaulting to 'Other'")
        return "Other"

    def _validate_and_clean_child_data(self, child: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean child data fields."""
        # Validate parish
        if child.get("parish") and child["parish"] not in self.VALID_PARISHES:
            logger.warning(f"Invalid parish: {child['parish']}")
            child["parish"] = None
        
        # Validate and format age
        age = child.get("age")
        if age:
            try:
                age_num = int(str(age).strip())
                if 0 <= age_num <= 25:
                    child["age"] = f"{age_num:02d}"
                else:
                    child["age"] = None
            except (ValueError, TypeError):
                child["age"] = None
        
        # Validate vulnerable groups
        if "vulnerableGroups" in child:
            if isinstance(child["vulnerableGroups"], list):
                child["vulnerableGroups"] = [
                    vg for vg in child["vulnerableGroups"] 
                    if vg in self.VALID_VULNERABLE_GROUPS
                ]
                if not child["vulnerableGroups"]:
                    child["vulnerableGroups"] = None
            else:
                child["vulnerableGroups"] = None
        
        # Validate region
        if child.get("region") and child["region"] not in self.VALID_REGIONS:
            child["region"] = None
        
        # Normalize living situation to match Pydantic enum
        if child.get("livingSituation"):
            child["livingSituation"] = self._normalize_living_situation(child["livingSituation"])
        
        # Keep gender as-is (no validation)
        
        return child

    def _extract_age_from_text(self, text: str) -> Optional[str]:
        """Extract age from conversation text using regex."""
        age_match = re.search(
            r'\b([0-9]|1[0-9]|2[0-5])\s*(?:year(?:s)?\s*old|yo|y/o|years?)\b', 
            text, 
            re.IGNORECASE
        )
        if age_match:
            age_num = int(age_match.group(1))
            return f"{age_num:02d}"
        return None

    def _apply_smart_defaults(self, child: Dict[str, Any], full_text: str) -> Dict[str, Any]:
        """Apply reasonable inferences to fill missing data."""
        # Infer nationality from Jamaican parish
        if not child.get("nationality") and child.get("parish"):
            if child["parish"] in self.VALID_PARISHES:
                child["nationality"] = "Jamaican"
                logger.info("Inferred nationality 'Jamaican' from parish")
        
        # Infer region from parish
        if not child.get("region") and child.get("parish"):
            parish = child["parish"]
            cities = {"Kingston", "St. Andrew"}
            rural = {"Portland", "St. Mary", "St. Elizabeth", "Manchester", "Clarendon"}
            
            if parish in cities:
                child["region"] = "Cities"
            elif parish in rural:
                child["region"] = "Rural areas"
            else:
                child["region"] = "Town & semi-dense areas"
            logger.info(f"Inferred region from parish '{parish}'")
        
        return child

    async def extract_form_data(self, messages: List[ChatMessage]) -> AutoFillResponse:
        """Extract structured form data from conversation using LLM."""
        full_text = "\n".join(
            f"[{msg.sender.upper()}]: {msg.message}" 
            for msg in messages
        )

        system_prompt = self._build_extraction_prompt()
        
        api_messages = self._prepare_conversation_context(messages)
        api_messages.append({
            "role": "user", 
            "content": "Extract the structured form data as JSON. Remember: only include facts explicitly stated in the conversation."
        })

        try:
            raw_response = await self._make_request(
                api_messages, 
                system_prompt,
                temperature=0.1,
                max_tokens=2000
            )
            logger.info(f"LLM extraction response length: {len(raw_response)}")

            # Clean and parse JSON
            json_str = self._clean_json_response(raw_response)
            data = json.loads(json_str)

            # Extract sections
            child = data.get("child", {})
            summary = data.get("summary", {})
            category = data.get("category", {})

            # Validate and clean child data
            child = self._validate_and_clean_child_data(child)
            
            # Apply smart defaults to fill missing data
            child = self._apply_smart_defaults(child, full_text)

            # Fallback age extraction from text
            if not child.get("age"):
                extracted_age = self._extract_age_from_text(full_text)
                if extracted_age:
                    child["age"] = extracted_age
                    logger.info(f"Age extracted via regex: {extracted_age}")

            # Ensure keepConfidential defaults to True
            if summary.get("keepConfidential") is None:
                summary["keepConfidential"] = True

            return AutoFillResponse(
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
                suggested_categories=category if isinstance(category, dict) else {}
            )

        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error in extract_form_data: {e}", exc_info=True)
            return AutoFillResponse()
        except Exception as e:
            logger.error(f"extract_form_data error: {e}", exc_info=True)
            return AutoFillResponse()

    def _build_extraction_prompt(self) -> str:
        """Build the system prompt for data extraction."""
        return (
            "You are a data extraction assistant for a child helpline. "
            "Your task is to read the FULL conversation and extract ONLY facts that are clearly and explicitly stated.\n\n"
            
            "CRITICAL RULES:\n"
            "- Do NOT guess, infer, assume, or make up any information\n"
            "- If a detail is not explicitly mentioned, use null\n"
            "- Be conservative: when in doubt, use null\n"
            "- Extract exact phrases where possible\n\n"
            
            "Return a valid JSON object with exactly these top-level keys: \"child\", \"category\", \"summary\".\n\n"
            
            "CHILD OBJECT:\n"
            "- firstName, lastName: extract only if full name is clearly stated\n"
            "- gender: extract as stated (any value is acceptable)\n"
            "- age: extract numeric age if stated (format as two digits: '05', '14', etc.)\n"
            f"- parish: must be one of: {', '.join(sorted(self.VALID_PARISHES))}\n"
            "- streetAddress: full address if provided\n"
            "- phone1, phone2: Jamaican phone numbers if shared\n"
            "- nationality: if explicitly stated (e.g., 'Jamaican')\n"
            "- schoolName, gradeLevel: only if explicitly named\n"
            "- livingSituation: MUST be one of these exact values: 'With parent(s)', 'With relatives', 'Alternative care', 'Group residential facility', 'Homeless or marginally housed', 'In detention', 'Living independently', 'Other', 'Unknown'\n"
            f"- vulnerableGroups: array of items from this exact set: {json.dumps(list(self.VALID_VULNERABLE_GROUPS))}\n"
            f"- region: one of {', '.join(sorted(self.VALID_REGIONS))}\n\n"
            
            "CATEGORY OBJECT:\n"
            "Group issues under category keys (e.g., \"Violence\", \"Mental Health\", \"Family Relationships\"). "
            "Each value is an array of specific issue labels mentioned. If no categories discussed, return {}.\n\n"
            
            "SUMMARY OBJECT:\n"
            "- callSummary: brief 1-2 sentence summary of the main issue\n"
            "- keepConfidential: always true\n"
            "- Other fields (repeatCaller, actionTaken, etc.): null unless explicitly stated\n\n"
            
            "OUTPUT REQUIREMENTS:\n"
            "- Return ONLY valid JSON\n"
            "- No markdown, no code blocks, no explanations\n"
            "- Start with { and end with }\n"
            "- Use double quotes for strings\n"
            "- Use null (not 'null' or 'None') for missing values"
        )

    async def generate_summary(self, messages: List[ChatMessage]) -> str:
        """Generate professional conversation summary."""
        system_prompt = (
            "You are a professional child helpline case worker. "
            "Write a concise, factual, and empathetic summary of the conversation for case records.\n\n"
            "Include:\n"
            "- Main issue or concern raised\n"
            "- Child's age and gender (if known)\n"
            "- Location (if mentioned)\n"
            "- Key risk factors or vulnerabilities\n"
            "- Child's expressed needs or requests\n"
            "- Any immediate safety concerns\n\n"
            "Requirements:\n"
            "- Keep it under 4 sentences\n"
            "- Use neutral, professional language\n"
            "- State only facts from the conversation\n"
            "- Do not include speculation or assumptions\n"
            "- Be sensitive to the child's situation"
        )

        api_messages = self._prepare_conversation_context(messages)
        api_messages.append({
            "role": "user",
            "content": "Please write a professional case summary of this conversation for our records."
        })

        try:
            summary = await self._make_request(
                api_messages, 
                system_prompt,
                temperature=0.3,
                max_tokens=500
            )
            return summary.strip()
        except Exception as e:
            logger.error(f"Failed to generate summary: {str(e)}", exc_info=True)
            return "Summary could not be generated due to a technical error."
    
    async def extract_conversation_metadata(self, messages: List[ChatMessage]) -> Dict[str, Any]:
        """Extract metadata that can be inferred from conversation."""
        full_text = "\n".join(f"[{msg.sender.upper()}]: {msg.message}" for msg in messages)
        
        system_prompt = (
            "Analyze this child helpline conversation and extract metadata as JSON.\n\n"
            "Fields to extract (use null if not present):\n"
            "- locationOfIssue: where issue occurs ('At school', 'At home', 'Online', 'In the community', 'Other')\n"
            "- actionTaken: what counselor did ('Provided emotional support', 'Made referral', 'Gave advice', 'Active listening', 'Escalated to protection services')\n"
            "- outcomeOfContact: how call ended ('Issue resolved', 'Referral made', 'Follow-up needed', 'Child felt heard', 'Call disconnected')\n"
            "- howDidYouKnowAboutOurLine: how they found helpline ('School', 'Friend', 'Social media', 'Internet search', 'Advertisement', 'Other')\n"
            "- okForCaseWorkerToCall: true/false/null - did child give permission for follow-up call?\n"
            "- didTheChildFeelWeSolvedTheirProblem: true/false/null - did child express satisfaction or problem resolution?\n"
            "- wouldTheChildRecommendUsToAFriend: true/false/null - did child express they would recommend service?\n"
            "- didYouDiscussRightsWithTheChild: true/false - did counselor discuss children's rights?\n\n"
            "RULES:\n"
            "- Analyze the ENTIRE conversation carefully\n"
            "- Use null if information not clearly present\n"
            "- For boolean fields, use true/false/null (not strings)\n"
            "- Infer reasonably from conversation context\n"
            "- Output ONLY valid JSON, no markdown or explanations"
        )
        
        api_messages = [{"role": "user", "content": full_text}]
        
        try:
            response = await self._make_request(
                api_messages, 
                system_prompt, 
                temperature=0.2,
                max_tokens=800
            )
            json_str = self._clean_json_response(response)
            metadata = json.loads(json_str)
            logger.info(f"Extracted conversation metadata: {json.dumps(metadata, indent=2)}")
            return metadata
        except Exception as e:
            logger.error(f"Failed to extract metadata: {e}", exc_info=True)
            return {}


# Singleton instance
llm_service = LLMService()