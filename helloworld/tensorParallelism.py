## Try Deepspeed inference
## To run this on cpu
## Navingate to the file path
## deepspeed --bind_cores_to_rank tensorParallelism.py
import os
import torch
import transformers
import deepspeed

# FlanT5
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import AutoConfig, AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import AutoModelForCausalLM, AutoTokenizer

# Set the device
device = (
        "cuda"
        if torch.cuda.is_available()
        else "mps" if torch.backends.mps.is_available() else "cpu"
    )

# Deepspeed will set local rank and world size
local_rank = int(os.getenv("LOCAL_RANK", "0"))
world_size = int(os.getenv("WORLD_SIZE", "1"))

def deepspeedInf(model, tokenizer):
    pipe = transformers.pipeline(task="text2text-generation", model=model, tokenizer=tokenizer, device=local_rank)
    pipe.model = deepspeed.init_inference(
        pipe.model,
        mp_size=world_size,
        dtype=torch.float
    )
    return pipe

def generalInf(prompt, model, tokenizer):
    # Apply chat template
    messages = [{"role": "user", "content": prompt}]
    formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False)

    # Tokenize the input
    inputs = tokenizer(formatted_prompt, return_tensors="pt").to(device)

    # Generate output
    outputs = model.generate(**inputs, max_new_tokens=100)
    # Decode the result
    decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(decoded_output)

def localModel(device):
    mp = r'/home/nachiketa/Documents/Workspaces/checkpoints/smolLM2-135M-Instruct'
    model = AutoModelForCausalLM.from_pretrained(pretrained_model_name_or_path=mp).to(device)
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=mp)
    return  tokenizer, model

def flanT5():
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large")
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large")
    return tokenizer, model

def t5small():
    tokenizer = T5Tokenizer.from_pretrained("google/t5-v1_1-small")
    # Load in bfloat16
    config = AutoConfig.from_pretrained("google/t5-v1_1-small")
    model = AutoModelForSeq2SeqLM.from_pretrained(
        "google/t5-v1_1-small",
        config=config
        #dtype=torch.bfloat16
    )
    return tokenizer, model

prompt = "Translate the following English text to spanish: 'You are gorgeous'"
#prompt = "Write a haiku about programming"

# Use the model local to the machine
#tokenizer, model = localModel(device)

# General inference
#generalInf(prompt, model, tokenizer)

# Deepspeed Inference
#pipe = deepspeedInf(model, tokenizer)
#output = pipe(prompt)
#print(output)

# FlanT5 google model
tokenizer, model = flanT5()

# Deepspeed Inference
pipe = deepspeedInf(model, tokenizer)
output = pipe(prompt)
print(output)

# Google T5 small
tokenizer, model = t5small()
pipe = deepspeedInf(model, tokenizer)
output = pipe(prompt)
print(output)