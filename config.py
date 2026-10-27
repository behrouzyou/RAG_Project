import os

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")
RULES_FILE="data/rules.txt"
CHUNK_SIZE=800
VECTOR_DB_PATH = 'db/vectors.db'
VECTOR_COLLECTION_NAME="rules"