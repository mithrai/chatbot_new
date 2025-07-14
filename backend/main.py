from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import get_bot_response 

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    message: str

@app.post("/chat")
def chat(user_input: UserInput):
    response = get_bot_response(user_input.message)
    return {"response": response}
