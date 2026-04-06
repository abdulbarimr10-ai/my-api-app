import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://my-api-app-sigma.vercel.app",  # Your current active Vercel link
    "https://my-api-app-bari2.vercel.app",  # Any other aliases you have
]

# --- THE SECURITY GUARD (CORS) ---
# In production, replace ["*"] with ["https://your-frontend.vercel.app"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "Backend is Live"}

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("AI-Logger")

app = FastAPI()

@app.post("/chat")
async def chat(query: Query):
    start_time = time.time() # Track how long the AI takes
    
    # LOG 1: The Input
    logger.info(f"--- NEW REQUEST ---")
    logger.info(f"USER INPUT: {query.text}")

    try:
        # Simulate your AI Logic
        # (Replace this with your actual Groq/OpenAI call)
        response_text = f"AI processed: {query.text}"
        
        # LOG 2: The Success & Timing
        duration = round(time.time() - start_time, 2)
        logger.info(f"RESPONSE GENERATED IN: {duration}s")
        logger.info(f"FINAL OUTPUT: {response_text[:50]}...") # Log first 50 chars
        
        return {"response": response_text}

    except Exception as e:
        # LOG 3: The Failure
        logger.error(f"SYSTEM CRASHED ON INPUT: {query.text}")
        logger.error(f"ERROR DETAIL: {str(e)}", exc_info=True) # exc_info shows the exact line number
        
        raise HTTPException(status_code=500, detail="Internal AI Error")

if __name__ == "__main__":
    import uvicorn
    # Use the PORT environment variable assigned by Railway
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
