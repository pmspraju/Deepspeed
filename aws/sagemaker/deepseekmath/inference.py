## Try Deepspeed inference
## To run this on cpu
## Navingate to the file path
## deepspeed --bind_cores_to_rank tensorParallelism.py
import os
import torch
import transformers
import deepspeed
from gptqmodel import GPTQModel

from transformers import AutoConfig, AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

print("Torch version:", torch.__version__)
print("CUDA Available:", torch.cuda.is_available())
print("CUDA Version:", torch.version.cuda)
print("GPU Count:", torch.cuda.device_count())
print("GPU Name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU detected")

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
    pipe = transformers.pipeline(task="text-generation", model=model, tokenizer=tokenizer)
    pipe.model = deepspeed.init_inference(
        pipe.model,
        mp_size=world_size,
        dtype=torch.float
    )
    return pipe

def generalInf(prompt, model, tokenizer):
    # Apply chat template
    messages = [{"role": "user", "content": prompt}]
    #formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False)
    formatted_prompt = prompt

    # Tokenize the input
    inputs = tokenizer(formatted_prompt, return_tensors="pt")

    # Generate output
    outputs = model.generate(**inputs, max_new_tokens=100)
    # Decode the result
    decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(decoded_output)

def localModel(device):
    mp = r'/home/nachiketa/Documents/Workspaces/checkpoints/deepseekmath/base'
    #mp = r'/home/nachiketa/Documents/Workspaces/checkpoints/deepseekmath/gptq_int4'
    #mp = r'/home/nachiketa/Documents/Workspaces/checkpoints/deepseekmath/gptq_int8'
    #model = GPTQModel.load(mp)
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=mp)
    model = AutoModelForCausalLM.from_pretrained(mp, torch_dtype=torch.bfloat16)#.to(device)
    model.generation_config = GenerationConfig.from_pretrained(mp)
    model.generation_config.pad_token_id = model.generation_config.eos_token_id
    return  tokenizer, model

# Main logic
prompt = "A farmer has 30 chickens, 20 ducks, and 15 geese. If the farmer loses 5 chickens and 3 geese, how many birds does the farmer have in total now?"
#prompt = "The integral of x^2 from 0 to 2 is"

# Use the model local to the machine
tokenizer, model = localModel(device)

# General inference
#generalInf(prompt, model, tokenizer)

# Deepspeed Inference
pipe = deepspeedInf(model, tokenizer)
output = pipe(prompt)
print(output)

# Initialize DeepSpeed inference engine
#ds_engine = deepspeed.init_inference(model, dtype=torch.half, replace_with_kernel_inject=True)

# Run inference
#text = "Solve for x: 2x + 5 = 15"
#inputs = tokenizer(text, return_tensors="pt").to("cuda")
#output = ds_engine.module.generate(**inputs)
#print(tokenizer.decode(output[0], skip_special_tokens=True))