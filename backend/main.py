from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running!"}

class Message(BaseModel):
    message: str

@app.post("/chat")
def chat_endpoint(msg: Message):
    user_message = msg.message
    # You can replace this with your actual model logic
    return {"response": f"Echo: {user_message}"}
