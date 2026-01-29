from dotenv import load_dotenv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

print("DATABASE_URL =", os.getenv("DATABASE_URL"))
print("BETTER_AUTH_SECRET =", os.getenv("BETTER_AUTH_SECRET"))
print("BETTER_AUTH_URL =", os.getenv("BETTER_AUTH_URL"))
