from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn
from llm.llm import LocalModelTransformers
from llm.ai_war import AIWar
from fastapi.middleware.cors import CORSMiddleware

MODEL_NAME = "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit"

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
    model = LocalModelTransformers(MODEL_NAME)
    app.state.model = model
    print("Model loaded")

class GenerationRequest(BaseModel):
    data: dict

class GenerationResponse(BaseModel):
    generated_json: dict

@app.post("/first-reinforcement", response_model=GenerationResponse)
async def generate_play_endpoing(request: GenerationRequest):
    ai = AIWar(app.state.model)
    generated_json = ai.first_reinforcement(
        player_data=request.data
    )
    return {"generated_json": generated_json}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
