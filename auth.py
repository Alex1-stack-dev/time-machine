import os
from fastapi import Header, HTTPException, status, Depends
from dotenv import load_dotenv

load_dotenv()  # loads .env if present

API_KEY = os.getenv("API_KEY", None)
if not API_KEY:
    # In development allow an obvious default but we will log a warning in server on startup
    API_KEY = "change-me"

def require_api_key(x_api_key: str = Header(None)):
    if x_api_key is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing API key")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key")
    return True

def get_api_key_for_docs():
    # helpful for docs/examples
    return {"header": "x-api-key", "value": API_KEY}
