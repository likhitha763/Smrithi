import os
from dotenv import load_dotenv

load_dotenv()

# Firebase Admin SDK — service account credentials
# Primary: path to serviceAccountKey.json file (preferred for local dev)
FIREBASE_CRED_PATH = os.getenv("FIREBASE_CRED_PATH", "serviceAccountKey.json")

# Fallback: individual env vars (used when JSON file is absent — e.g. CI, smoke test)
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "")
FIREBASE_CLIENT_EMAIL = os.getenv("FIREBASE_CLIENT_EMAIL", "")
FIREBASE_PRIVATE_KEY = os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n")

# Firebase Web API Key — used only by smoke_test.py (Auth REST API)
FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY", "")

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")