import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://my-api-app-bari2.vercel.app", # Add your actual Vercel link here
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

@app.post("/chat")
async def chat(query: Query):
    # This is where your AI logic lives
    return {"response": f"AI processed: {query.text}"}

if __name__ == "__main__":
    import uvicorn
    # Use the PORT environment variable assigned by Railway
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
