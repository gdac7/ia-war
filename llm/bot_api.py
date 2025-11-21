from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn
from llm.llm import LocalModel
from llm.ai_war import AIWar
from fastapi.middleware.cors import CORSMiddleware
import time
import json
import os
MODEL_NAME_TRANSFORMERS = "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit"

app = FastAPI(title="bot-war")
origins = [
    "http://localhost:8081",  
    "http://localhost:8080",  
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      
    allow_credentials=True,
    allow_methods=["*"],         
    allow_headers=["*"],         
)

@app.on_event("startup")
def load_models():
    print("Loading model...")
    model = LocalModel(transformers=False, bnb_config=False)
    app.state.model = model
    app.state.bot_count = 0
    analysis_path = "analysis/tesponse_time.json"
    if os.path.exists(analysis_path):
        with open(analysis_path, "r") as f:
            app.state.response_bot_time = json.load(f)
    else:
        app.state.response_bot_time = []
    print("Model loaded")

class GenerationRequest(BaseModel):
    data: dict

class GenerationResponse(BaseModel):
    generated_json: dict

@app.post("/first-reinforcement", response_model=GenerationResponse)
async def generate_play_endpoint(request: GenerationRequest):
    start = time.time()
    ai = AIWar(app.state.model)
    generated_json = ai.first_reinforcement(
        player_data=request.data
    )
    duration_time = time.time() - start
    info = {
            "bot": (app.state.bot_count % 4) + 1,
            "time": duration_time,
    }
    app.state.response_bot_time.append(info)
    with open("analysis/response_time.json", "w") as f:
        json.dump(app.state.response_bot_time, f, indent=4)
    

    return {"generated_json": generated_json, "duration_time": f"{duration_time:.2f}s"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
