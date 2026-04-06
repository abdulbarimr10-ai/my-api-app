import os
import time
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 1. LOGGING CONFIGURATION
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("AI-Logger")

app = FastAPI()

# 2. CORS SECURITY
origins = [
    "http://localhost:3000",
    "https://my-api-app-sigma.vercel.app", 
    "https://my-api-app-bari2.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. DATA MODELS
class Query(BaseModel):
    text: str

# 4. EVALUATION LOGIC (The RAGAS Mindset)
def run_simple_eval(user_input, ai_response):
    score = 0
    feedback = []

    # Check 1: Length (Faithfulness to detail)
    if len(ai_response) > 20:
        score += 1
    else:
        feedback.append("Response might be too brief.")

    # Check 2: Keyword Match (Relevance)
    input_keywords = set(user_input.lower().split())
    matches = [word for word in input_keywords if word in ai_response.lower()]
    if len(matches) > 0:
        score += 1
    else:
        feedback.append("Response doesn't seem to reference input keywords.")

    return score, feedback

# 5. ROUTES
@app.get("/")
def home():
    return {"status": "Backend is Live"}

@app.post("/chat")
async def chat(query: Query):
    start_time = time.time()
    
    logger.info(f"--- NEW REQUEST ---")
    logger.info(f"USER INPUT: {query.text}")

    try:
        # --- AI LOGIC START ---
        # Note: Replace this simulation with your actual LLM call later
        ai_response = f"AI processed: {query.text}" 
        # --- AI LOGIC END ---

        # Evaluation & Metrics
        duration = round(time.time() - start_time, 2)
        quality_score, quality_feedback = run_simple_eval(query.text, ai_response)
        
        # Logging findings
        logger.info(f"RESPONSE TIME: {duration}s")
        logger.info(f"EVAL SCORE: {quality_score}/2 | FEEDBACK: {quality_feedback}")
        logger.info(f"FINAL OUTPUT: {ai_response[:50]}...")

        return {
            "response": ai_response,
            "eval_score": quality_score,
            "metadata": {"latency": duration}
        }

    except Exception as e:
        logger.error(f"SYSTEM CRASHED ON INPUT: {query.text}")
        logger.error(f"ERROR DETAIL: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal AI Error")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
