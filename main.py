from fastapi import FastAPI, HTTPException
import requests
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import os

from downloadRequestModel import DownloadRequest

# Load environment variables from .env file
load_dotenv()

# Access the variables
database_url = os.getenv('DATABASE_URL')

app = FastAPI()

# Configure CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["post", "get"],
    allow_headers=["*"],
)

# Your RapidAPI configuration
RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST')
RAPIDAPI_ENDPOINT = os.getenv('RAPIDAPI_ENDPOINT')
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')

@app.get("/")
def read_root():
    return {"message": "Welcome to the Social Media Downloader API"}

@app.get("/api/download/{url:path}")
async def download_content(url: str):
    """
    Proxy endpoint for social media download
    """
    try:
        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": RAPIDAPI_HOST,
            "Content-Type": "application/json"
        }
        
        payload = {"url": url}
        
        # You could add caching here to avoid repeated requests for same URL
        
        response = requests.post(
            RAPIDAPI_ENDPOINT,
            json=payload,
            headers=headers
        )
        
        response.raise_for_status()  # Raise exception for HTTP errors
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error communicating with RapidAPI: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )
# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

