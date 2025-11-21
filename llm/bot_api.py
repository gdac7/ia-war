from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn
from llm.llm import LocalModel
from llm.ai_war import AIWar
from fastapi.middleware.cors import CORSMiddleware
import time
import json
from .utils import *

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
    print("Model loaded")

class GenerationRequest(BaseModel):
    data: dict

class GenerationResponse(BaseModel):
    generated_json: dict

@app.post("/reinforcement", response_model=GenerationResponse)
async def reinforcement_endpoint(request: GenerationRequest):
    start = time.time()
    ai = AIWar(app.state.model)
    specific_reinforcement_phase = request.data.pop("phase")
    stats_data = request.data.pop("botStats")
    generated_json = ai.reinforcement(
        player_data=request.data
    )
    duration_time = time.time() - start
    create_analysis_files(app)
    save_data(app, specific_reinforcement_phase, duration_time, stats_data)
    return {"generated_json": generated_json, "duration_time": f"{duration_time:.2f}s"}


@app.post("/attack", response_model=GenerationResponse)
async def attack_endpoint(request: GenerationRequest):
    start = time.time()
    ai = AIWar(app.state.model)
    stats_data = request.data.pop("botStats")
    generated_json = ai.attack(
        player_data=request.data
    )
    duration_time = time.time() - start
    save_data(app, "attack", duration_time, stats_data)
    return {"generated_json": generated_json, "duration_time": f"{duration_time:.2f}s"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
