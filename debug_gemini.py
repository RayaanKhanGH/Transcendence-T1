
import os
from dotenv import load_dotenv
from google import genai
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_gemini_connection():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in .env")
        return

    print(f"API Key found: {api_key[:5]}...{api_key[-5:]}")
    
    try:
        client = genai.Client(api_key=api_key)
        
        # 1. List available models
        print("\nListing available models...")
        try:
            # List models using the new client
            for model in client.models.list():
                print(f" - {model.name}")
        except Exception as e:
            print(f"Could not list models: {e}")

        # List of models to test
        models_to_test = [
            os.getenv("MODEL"), # Test the one in ENV first
            "gemini-2.5-flash", 
            "models/gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-2.0-flash-exp",
            "models/gemini-2.0-flash-exp",
            "gemini-1.5-flash",
            "gemini-1.5-flash-latest",
            "models/gemini-1.5-flash",
            "gemini-1.5-flash-002",
            "gemini-1.5-pro",
            "gemini-pro"
        ]

        with open("debug_result_clean.txt", "w", encoding="utf-8") as f:
            f.write(f"Testing {len(models_to_test)} models...\n")
            
            for model in models_to_test:
                f.write(f"\n--- Testing: {model} ---\n")
                try:
                    # Try generating content
                    response = client.models.generate_content(
                        model=model,
                        contents="Hi"
                    )
                    f.write(f"SUCCESS! ({model})\n")
                    f.write(f"Response: {response.text}\n")
                except Exception as e:
                    # simplify error message
                    err_str = str(e).replace('\n', ' ')[:300]
                    f.write(f"FAILED ({model}): {err_str}...\n")

    except Exception as e:
        print(f"❌ critical error initializing client: {e}")

if __name__ == "__main__":
    test_gemini_connection()
