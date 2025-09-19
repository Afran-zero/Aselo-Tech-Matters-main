import json
import asyncio
import aiofiles
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

from ..models.conversation_model import ConversationHistory, ChatMessage
from ..models.form_model import FormSubmission
from ..utils.error_handler import DatabaseException
from ..utils.logger import get_logger

logger = get_logger(__name__)


class DatabaseService:
    """Service for handling local JSON database operations"""

    def __init__(self, db_path: str = "database/local_db.json"):
        self.db_path = Path(__file__).parent.parent.parent / db_path
        self._lock = asyncio.Lock()
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """Ensure the database file exists with proper structure"""
        if not self.db_path.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            initial_data = {
                "conversations": {},
                "form_submissions": {},
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "version": "1.0.0",
                    "description": "Aselo Backend Local Database"
                }
            }
            self.db_path.write_text(json.dumps(initial_data, indent=2))
            logger.info(f"Initialized database at {self.db_path}")

    async def _read_db(self) -> Dict[str, Any]:
        """Read the entire database"""
        try:
            async with aiofiles.open(self.db_path, "r") as f:
                content = await f.read()
                return json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Database read error: {e}")
            raise DatabaseException(f"Failed to read database: {str(e)}")

    async def _write_db(self, data: Dict[str, Any]):
        """Write the entire database"""
        try:
            async with aiofiles.open(self.db_path, "w") as f:
                await f.write(json.dumps(data, indent=2, default=str))
        except Exception as e:
            logger.error(f"Database write error: {e}")
            raise DatabaseException(f"Failed to write database: {str(e)}")

    async def get_conversation(self, session_id: str) -> Optional[ConversationHistory]:
        """Get conversation history for a session (no external lock calls)"""
        db_data = await self._read_db()
        conversation_data = db_data.get("conversations", {}).get(session_id)

        if not conversation_data:
            return None

        messages = [
            ChatMessage(**msg_data) for msg_data in conversation_data.get("messages", [])
        ]

        return ConversationHistory(
            sessionId=conversation_data["sessionId"],
            messages=messages,
            created_at=datetime.fromisoformat(conversation_data["created_at"]),
            updated_at=datetime.fromisoformat(conversation_data["updated_at"])
        )

    async def save_conversation(self, conversation: ConversationHistory):
        """Save or update conversation history"""
        async with self._lock:
            db_data = await self._read_db()
            conversation_dict = {
                "sessionId": conversation.sessionId,
                "messages": [
                    {
                        "id": msg.id,
                        "sender": msg.sender,
                        "message": msg.message,
                        "timestamp": msg.timestamp.isoformat(),
                    }
                    for msg in conversation.messages
                ],
                "created_at": conversation.created_at.isoformat(),
                "updated_at": datetime.now().isoformat(),
            }
            db_data["conversations"][conversation.sessionId] = conversation_dict
            await self._write_db(db_data)

            logger.info(f"Saved conversation for session: {conversation.sessionId}")

    async def add_message_to_conversation(self, session_id: str, message: ChatMessage):
        """Add a single message to existing conversation or create new one"""
        async with self._lock:
            db_data = await self._read_db()
            conversations = db_data.setdefault("conversations", {})

            conversation = conversations.get(session_id)
            if conversation is None:
                # Create new conversation
                conversation = {
                    "sessionId": session_id,
                    "messages": [],
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                }
                conversations[session_id] = conversation

            conversation["messages"].append(message.dict())
            conversation["updated_at"] = datetime.now().isoformat()

            await self._write_db(db_data)
            logger.info(f"Added message to session {session_id}: {message.sender}")

    async def get_form_submission(self, session_id: str) -> Optional[FormSubmission]:
        db_data = await self._read_db()
        submission_data = db_data.get("form_submissions", {}).get(session_id)
        return FormSubmission(**submission_data) if submission_data else None

    async def save_form_submission(self, submission: FormSubmission):
        async with self._lock:
            db_data = await self._read_db()
            submission_dict = {
                "sessionId": submission.sessionId,
                "submissionId": submission.submissionId,
                "formData": submission.formData.dict(),
                "submitted_at": submission.submitted_at.isoformat(),
                "status": submission.status,
            }
            db_data["form_submissions"][submission.sessionId] = submission_dict
            await self._write_db(db_data)

            logger.info(f"Saved form submission for session: {submission.sessionId}")

    async def list_conversations(self) -> List[str]:
        db_data = await self._read_db()
        return list(db_data.get("conversations", {}).keys())

    async def list_form_submissions(self) -> List[str]:
        db_data = await self._read_db()
        return list(db_data.get("form_submissions", {}).keys())

    async def delete_conversation(self, session_id: str) -> bool:
        async with self._lock:
            db_data = await self._read_db()
            conversations = db_data.get("conversations", {})
            if session_id in conversations:
                del conversations[session_id]
                await self._write_db(db_data)
                logger.info(f"Deleted conversation for session: {session_id}")
                return True
            return False

    async def delete_form_submission(self, session_id: str) -> bool:
        async with self._lock:
            db_data = await self._read_db()
            submissions = db_data.get("form_submissions", {})
            if session_id in submissions:
                del submissions[session_id]
                await self._write_db(db_data)
                logger.info(f"Deleted form submission for session: {session_id}")
                return True
            return False


# Global database service instance
db_service = DatabaseService()
