from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn
from llm.llm import LocalModel
from llm.ai_war import AIWar
from fastapi.middleware.cors import CORSMiddleware
import time
import json
import os
from .utils import *

stats_app = FastAPI(title="bot-stats")

origins = [
    "http://localhost:8081",  
    "http://localhost:8082",  
]

stats_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      
    allow_credentials=True,
    allow_methods=["*"],         
    allow_headers=["*"],         
)

@stats_app.on_event("startup")
def load_path():
    stats_app.state.stats_path = "analysis/stats.json"

    
class GenerationRequest(BaseModel):
    data: dict

class GenerationResponse(BaseModel):
    data: dict
@stats_app.post("/stats", response_model=GenerationResponse)
async def stats_endpoint(request: GenerationRequest):
    stats = request.data
    with open(stats_app.state.stats_path, "w") as f:
        json.dump(stats, f, indent=4)
    return {"data": stats}

if __name__ == "__main__":
    uvicorn.run(stats_app, host="0.0.0.0", port=8082)

