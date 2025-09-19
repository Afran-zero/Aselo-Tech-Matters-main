# Aselo Backend API

A production-ready, modular FastAPI backend for chatbot and form processing with OpenRouter LLM integration.

## 🚀 Features

- **Chat API** (`/api/chat`): Process chat messages with AI-powered responses
- **Auto-Fill** (`/api/autofill`): Extract structured form data from conversations
- **Summarization** (`/api/summarize`): Generate conversation summaries
- **Form Submission** (`/api/submitForm`): Handle form data submissions
- **Local JSON Database**: File-based storage with async operations
- **Comprehensive Error Handling**: Custom exceptions and middleware
- **Structured Logging**: Color-coded logs with proper formatting
- **API Documentation**: Auto-generated OpenAPI docs

## 📁 Project Structure

```
backend/
├── app/
│   ├── controllers/          # Business logic controllers
│   │   ├── chat_controller.py
│   │   └── form_controller.py
│   ├── models/              # Pydantic data models
│   │   ├── conversation_model.py
│   │   └── form_model.py
│   ├── routes/              # FastAPI route definitions
│   │   ├── chat_routes.py
│   │   └── form_routes.py
│   ├── services/            # External service integrations
│   │   ├── db_service.py
│   │   └── llm_service.py
│   └── utils/               # Utility modules
│       ├── error_handler.py
│       └── logger.py
├── database/
│   └── local_db.json       # Local JSON database
├── main.py                 # FastAPI application entry point
├── run.py                  # Convenient runner script
└── requirements.txt        # Python dependencies
```

## 🛠️ Installation

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   
   Create a `.env` file in the backend directory:
   ```bash
   # Copy the template file
   cp env.template .env
   ```
   
   Then edit `.env` with your actual values:
   ```env
   # OpenRouter API Configuration
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   OPENROUTER_MODEL=openai/gpt-oss-120b:free
   
   # Server Configuration
   HOST=0.0.0.0
   PORT=8001
   RELOAD=true
   
   # Site Information for OpenRouter Rankings (Optional)
   SITE_URL=https://your-site-url.com
   SITE_NAME=Aselo Backend
   ```

## 🏃‍♂️ Running the Server

### Option 1: Using the runner script
```bash
python run.py
```

### Option 2: Using main.py directly
```bash
python main.py
```

### Option 3: Using uvicorn directly
```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

## 📊 API Endpoints

### Chat Endpoints

#### POST `/api/chat`
Process a chat message and get AI response.

**Request:**
```json
{
  "sessionId": "unique-session-id",
  "message": "Hello, I need help with a form"
}
```

**Response:**
```json
{
  "response": "Hi! I'd be happy to help you with that form. What information do you need to provide?"
}
```

#### POST `/api/autofill`
Extract structured data from conversation.

**Request:**
```json
{
  "sessionId": "unique-session-id"
}
```

**Response:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-555-0123",
  "address": "123 Main St, Anytown, USA",
  "notes": "Prefers morning appointments"
}
```

#### POST `/api/summarize`
Generate conversation summary.

**Request:**
```json
{
  "sessionId": "unique-session-id"
}
```

**Response:**
```json
{
  "summary": "User inquired about form assistance. Provided personal details including contact information and scheduling preferences."
}
```

### Form Endpoints

#### POST `/api/submitForm`
Submit form data for a session.

**Request:**
```json
{
  "sessionId": "unique-session-id",
  "formData": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-0123",
    "address": "123 Main St, Anytown, USA",
    "notes": "Additional information"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Form submitted successfully",
  "submissionId": "submission-uuid"
}
```

### Utility Endpoints

#### GET `/`
API information and available endpoints.

#### GET `/health`
Health check with service status.

#### GET `/docs`
Interactive API documentation (Swagger UI).

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | - | **Required** OpenRouter API key |
| `OPENROUTER_MODEL` | `openai/gpt-oss-120b:free` | LLM model to use |
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8001` | Server port |
| `RELOAD` | `true` | Enable auto-reload in development |
| `LOG_LEVEL` | `INFO` | Logging level |
| `SITE_URL` | - | Optional site URL for OpenRouter rankings |
| `SITE_NAME` | `Aselo Backend` | Optional site name for OpenRouter rankings |

### Database

The application uses a local JSON file (`database/local_db.json`) for data storage. The database is automatically initialized on first run.

## 🔒 Security Features

- **CORS Configuration**: Configurable cross-origin resource sharing
- **Input Validation**: Pydantic models for request/response validation
- **Error Handling**: Comprehensive exception handling with sanitized error responses
- **Logging**: Detailed logging for monitoring and debugging

## 🧪 Development

### Running in Development Mode
```bash
# With auto-reload enabled
python run.py

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Project Architecture

The backend follows a clean architecture pattern:

- **Routes**: Handle HTTP requests and responses
- **Controllers**: Contain business logic
- **Services**: Handle external integrations (database, LLM)
- **Models**: Define data structures
- **Utils**: Provide common functionality

## 📝 Error Handling

The API uses structured error responses:

```json
{
  "error": true,
  "message": "Human-readable error message",
  "error_code": "ERROR_TYPE",
  "status_code": 400
}
```

Common error codes:
- `VALIDATION_ERROR`: Invalid input data
- `SESSION_NOT_FOUND`: Session ID not found
- `LLM_ERROR`: LLM service error
- `DATABASE_ERROR`: Database operation error

## 🔗 Dependencies

- **FastAPI**: Modern, fast web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation and settings management
- **OpenAI**: Official OpenAI SDK for API calls
- **aiofiles**: Async file operations
- **python-dotenv**: Environment variable management

## 📞 Support

For issues or questions, please check the logs for detailed error information. The API provides comprehensive error messages and logging to help with troubleshooting.
