#!/usr/bin/env python3
"""
Aselo Backend Setup Script

This script helps set up the Aselo backend environment.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_path = Path(".env")
    template_path = Path("env.template")
    
    if env_path.exists():
        print("✅ .env file already exists")
        return True
    
    if template_path.exists():
        try:
            with open(template_path, 'r') as template:
                content = template.read()
            
            with open(env_path, 'w') as env_file:
                env_file.write(content)
            
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env and add your OPENROUTER_API_KEY")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("❌ env.template file not found")
        return False

def main():
    """Main setup function"""
    print("🚀 Aselo Backend Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        print("⚠️  You may need to manually create a .env file")
    
    # Initialize database
    db_path = Path("database/local_db.json")
    if not db_path.exists():
        db_path.parent.mkdir(exist_ok=True)
        with open(db_path, 'w') as f:
            f.write('{\n  "conversations": {},\n  "form_submissions": {},\n  "metadata": {\n    "created_at": "2025-09-15T00:00:00Z",\n    "version": "1.0.0"\n  }\n}')
        print("✅ Initialized database file")
    else:
        print("✅ Database file already exists")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📝 Next steps:")
    print("1. Edit .env file and add your OPENROUTER_API_KEY")
    print("2. Run: python run.py")
    print("3. Visit: http://localhost:8001/docs")
    
    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY") == "your_openrouter_api_key_here":
        print("\n⚠️  WARNING: OPENROUTER_API_KEY not configured!")
        print("   Please edit .env file and add your API key")

if __name__ == "__main__":
    main()
