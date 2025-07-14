from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return JSONResponse(content={"message": "Chatbot backend is running!"})

class Message(BaseModel):
    message: str

generator = pipeline("text-generation", model="sshleifer/tiny-gpt2")

@app.post("/chat")
def chat(msg: Message):
    user_input = msg.message
    response = generator(user_input, max_length=50, num_return_sequences=1)
    generated_text = response[0]['generated_text']
    return {"response": generated_text}
