import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 480))
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DEVICE_API_KEY = os.getenv("DEVICE_API_KEY")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
