from dotenv import load_dotenv
import os
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
VECTOR_DB_API_KEY = os.getenv("PINECONE_API_KEY")
POSTGRES_URI = os.getenv("POSTGRES_URI")