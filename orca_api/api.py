import torch
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

device = "cuda"

model = AutoModelForCausalLM.from_pretrained(
    "Open-Orca/Mistral-7B-OpenOrca").to(device)
tokenizer = AutoTokenizer.from_pretrained(
    "Open-Orca/Mistral-7B-OpenOrca")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SystemUserChatModel(BaseModel):
    system_prompt: str
    user_prompt: str

@app.post("/orca/qa")
async def generate_text(input_text: str):
    try:
        inputs = tokenizer(input_text, return_tensors="pt").to(device)
        outputs = model.generate(
            **inputs, max_new_tokens=256, use_cache=True, do_sample=True,
            temperature=0.2, top_p=0.95)
        generated_text = tokenizer.batch_decode(outputs)[0]
        return {"orca-response": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/orca/system-chat")
async def system_user_chat(body: SystemUserChatModel):
    system_prompt = body.system_prompt
    user_prompt = body.user_prompt
    try:
        prefix = ""
        suffix = "\n"
        sys_format = prefix + "system\n" + system_prompt + suffix
        user_format = prefix + "user\n" + user_prompt + suffix
        assistant_format = prefix + "assistant\n"
        input_text = sys_format + user_format + assistant_format

        generation_config = GenerationConfig(
            max_length=256, temperature=1.1, top_p=0.95, repetition_penalty=1.0,
            do_sample=True, use_cache=True,
            eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.eos_token_id,
            transformers_version="4.34.0.dev0")

        inputs = tokenizer(input_text, return_tensors="pt", return_attention_mask=True).to(device)
        outputs = model.generate(**inputs, generation_config=generation_config)

        generated_text = tokenizer.batch_decode(outputs)[0]
        return {"orca-response": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))