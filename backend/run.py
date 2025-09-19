#!/usr/bin/env python3
"""
Aselo Backend Runner Script

This script provides an easy way to run the Aselo backend with proper configuration.
"""

import os
import sys
import uvicorn
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Main entry point for running the server"""
    
    # Environment configuration with defaults
    config = {
        "app": "main:app",
        "host": os.getenv("HOST", "0.0.0.0"),
        "port": int(os.getenv("PORT", 8001)),
        "reload": os.getenv("RELOAD", "true").lower() == "true",
        "log_level": os.getenv("LOG_LEVEL", "info").lower()
    }
    
    print("🚀 Starting Aselo Backend API")
    print(f"📍 Server: http://{config['host']}:{config['port']}")
    print(f"📚 API Docs: http://{config['host']}:{config['port']}/docs")
    print(f"🔄 Reload: {config['reload']}")
    
    # Check for OpenRouter API key
    if not os.getenv("OPENROUTER_API_KEY"):
        print("⚠️  WARNING: OPENROUTER_API_KEY environment variable not set")
        print("   LLM features will not work without proper API key configuration")
    else:
        print("✅ OpenRouter API key configured")
    
    print("\n" + "="*50)
    
    # Start the server
    uvicorn.run(**config)

if __name__ == "__main__":
    main()
