import torch

from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig
from transformers import AutoTokenizer

print("Torch version:", torch.__version__)
print("CUDA Available:", torch.cuda.is_available())
print("CUDA Version:", torch.version.cuda)
print("GPU Count:", torch.cuda.device_count())
print("GPU Name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU detected")


device = "cuda" if torch.cuda.is_available() else "cpu"  # Detect GPU or fallback to CPU

base_path  = r'/home/nachiketa/Documents/Workspaces/checkpoints/deepseekmath/base'
save_mpath = r'/home/nachiketa/Documents/Workspaces/checkpoints/deepseekmath/gptq'

model_name = base_path

# Define quantization config
quant_config = BaseQuantizeConfig(
    bits=4,  # 4-bit quantization
    group_size=128,  # Group size for GPTQ
    desc_act=False  # Disable activation quantization
)

# Load the model for GPTQ quantization
quant_model = AutoGPTQForCausalLM.from_pretrained(model_name, quantize_config=quant_config).to(device)

# Load tokenizer (needed for example inputs)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Create example inputs
examples = tokenizer(["Solve the equation x^2 + 3x - 4 = 0"], return_tensors="pt").to(device)
#example_list = examples["input_ids"].tolist()  # Convert tensor to list
print(examples["input_ids"])

# Perform quantization before saving
quant_model.quantize([examples]).to(device)

# save the quantized model
quant_model.save_quantized(save_mpath)
