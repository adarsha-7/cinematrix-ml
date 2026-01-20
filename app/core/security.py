from fastapi import Header, HTTPException
from dotenv import load_dotenv
import os

load_dotenv()

def verify_api_key(api_key: str = Header(...)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(
            status_code=403,
            detail="Invalid or missing API key"
        )
