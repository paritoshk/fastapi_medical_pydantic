import uvicorn
import os
from dotenv import load_dotenv
import secrets

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Check for required environment variables and set defaults if needed
    if not os.getenv("SECRET_KEY"):
        print("WARNING: SECRET_KEY not found, generating a random one for this session")
        os.environ["SECRET_KEY"] = secrets.token_hex(32)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY not found in environment")
        print("The application will start but OpenAI API calls will fail")
        print("Please set your OPENAI_API_KEY in the .env file")
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Run the application with uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )

if __name__ == "__main__":
    main()