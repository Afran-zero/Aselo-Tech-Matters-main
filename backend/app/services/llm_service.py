from openai import AsyncOpenAI
import os, json, re
from typing import List, Optional
from ..models.conversation_model import ChatMessage, AutoFillResponse
from ..utils.error_handler import LLMException
from ..utils.logger import get_logger

logger = get_logger(__name__)

class LLMService:
    """Service for handling OpenRouter/OpenAI LLM API calls"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "openai/gpt-oss-120b:free")
        self.site_url = os.getenv("SITE_URL", "https://github.com/yourusername/aselo")
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

    async def _make_request(self, messages: List[dict], system_prompt: Optional[str] = None) -> str:
        """Call LLM API and return text response"""
        if not self.client:
            raise LLMException("LLM API key not configured", 500, "LLM_CONFIG_ERROR")

        api_messages = [{"role": "system", "content": system_prompt}] if system_prompt else []
        api_messages.extend(messages)

        try:
            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=api_messages,
                temperature=0.7,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                timeout=30.0,
                extra_headers={"HTTP-Referer": self.site_url, "X-Title": self.site_name}
            )
            if not completion.choices or not completion.choices[0].message:
                raise LLMException("No response from LLM", 500, "LLM_NO_RESPONSE")

            return completion.choices[0].message.content

        except Exception as e:
            logger.error(f"LLM API error: {str(e)}")
            raise LLMException(f"LLM request failed: {str(e)}", 500, "LLM_UNKNOWN_ERROR")

    def _prepare_conversation_context(self, messages: List[ChatMessage]) -> List[dict]:
        """Convert ChatMessage list to LLM-friendly message format"""
        api_messages = []
        for msg in messages:
            role = "user" if msg.sender == "user" else "assistant"
            api_messages.append({"role": role, "content": msg.message})
        return api_messages

    async def generate_chat_response(self, messages: List[ChatMessage], user_message: str) -> str:
        system_prompt = (
            "You are a helpful AI assistant for Aselo. Help users fill out forms via conversation. "
            "Keep responses friendly, concise, and guide the conversation to gather relevant info."
        )
        api_messages = self._prepare_conversation_context(messages)
        api_messages.append({"role": "user", "content": user_message})

        try:
            response = await self._make_request(api_messages, system_prompt)
            return response
        except LLMException:
            raise
        except Exception as e:
            raise LLMException(f"Failed to generate chat response: {str(e)}")

    async def extract_form_data(self, messages: List[ChatMessage]) -> AutoFillResponse:
        """Extract form data from conversation safely"""
        system_prompt = (
            "Extract form-relevant data from conversation. Return JSON with keys: "
            "name, email, phone, address, notes. Use null if not found."
        )
        api_messages = self._prepare_conversation_context(messages)
        api_messages.append({
            "role": "user",
            "content": "Please extract any form-relevant info from our conversation in JSON format."
        })

        try:
            raw_response = await self._make_request(api_messages, system_prompt)
            logger.info(f"LLM raw autofill response: {raw_response}")

            # Extract JSON using regex and parse
            json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(0))
            else:
                data = {}

            return AutoFillResponse(
                name=data.get("name"),
                email=data.get("email"),
                phone=data.get("phone"),
                address=data.get("address"),
                notes=data.get("notes")
            )
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM JSON: {str(e)}. Returning empty response.")
            return AutoFillResponse()
        except Exception as e:
            logger.error(f"Error in extract_form_data: {str(e)}")
            return AutoFillResponse()  # Always return empty on failure

    async def generate_summary(self, messages: List[ChatMessage]) -> str:
        """Generate concise conversation summary"""
        system_prompt = "Summarize the conversation concisely, highlighting key info and user requests."
        api_messages = self._prepare_conversation_context(messages)
        api_messages.append({"role": "user", "content": "Please provide a concise summary in plain text."})

        try:
            return await self._make_request(api_messages, system_prompt)
        except Exception as e:
            logger.error(f"Failed to generate summary: {str(e)}")
            return "Unable to generate summary."

# Singleton instance
llm_service = LLMService()
