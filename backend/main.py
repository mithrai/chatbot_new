from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

generator = pipeline("text-generation", model="sshleifer/tiny-gpt2")

@app.get("/")
def root():
    return {"message": "Chatbot backend is running."}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message")
    if not user_input:
        return {"response": "No message received."}

    result = generator(user_input, max_length=40, do_sample=True)
    return {"response": result[0]["generated_text"]}
