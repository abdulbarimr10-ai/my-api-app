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

# Configure logging to show time and severity
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.post("/chat")
async def chat(query: Query):
    logger.info(f"RECIEVED INPUT: {query.text}")
    try:
        # Simulate your AI logic
        response_text = f"AI processed: {query.text}"
        
        logger.info(f"FINAL OUTPUT: {response_text}")
        return {"response": response_text}
    except Exception as e:
        logger.error(f"SYSTEM FAILURE: {str(e)}", exc_info=True)
        return {"response": "I encountered an internal error."}

if __name__ == "__main__":
    import uvicorn
    # Use the PORT environment variable assigned by Railway
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
