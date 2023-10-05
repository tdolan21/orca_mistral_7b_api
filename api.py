# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM
from fastapi import FastAPI, Query, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import torch

device = torch.device('cuda:0')

# Load tokenizer and model and move model to GPU
tokenizer = AutoTokenizer.from_pretrained("Open-Orca/Mistral-7B-OpenOrca")
model = AutoModelForCausalLM.from_pretrained("Open-Orca/Mistral-7B-OpenOrca").to(device)

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to Mistral-7B-OpenOrca API. Testing is available at /docs."}

@app.post("/orca/")
async def orca_generate(input_text: str = Query(..., description="The input text to generate from")):
    try:
        # Tokenize and generate text
        input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)
        output = model.generate(input_ids, max_length=250)
        generated_text = tokenizer.decode(output[0].to('cuda:0'), skip_special_tokens=True)

        return {"generated_text": generated_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
