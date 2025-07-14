from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI()

# Load model and tokenizer
model_name = "microsoft/DialoGPT-small"  # You can change this to any lightweight chatbot model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# To keep track of conversation context
chat_history_ids = None

# Input message structure
class Message(BaseModel):
    message: str

@app.post("/chat")
def chat(msg: Message):
    global chat_history_ids

    # Encode the input
    new_input_ids = tokenizer.encode(msg.message + tokenizer.eos_token, return_tensors='pt')

    # Append to chat history (if any)
    bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids

    # Generate response
    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_k=50,
        top_p=0.95
    )

    # Decode response
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    return {"response": response}
