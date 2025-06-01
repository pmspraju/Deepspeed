import torch

from datasets import load_dataset
from gptqmodel import GPTQModel, QuantizeConfig

print("Torch version:", torch.__version__)
print("CUDA Available:", torch.cuda.is_available())
print("CUDA Version:", torch.version.cuda)
print("GPU Count:", torch.cuda.device_count())
print("GPU Name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU detected")

#set the device
device = "cuda" if torch.cuda.is_available() else "cpu"  # Detect GPU or fallback to CPU

#set the paths
base_path  = r'/home/nachiketa/Documents/Workspaces/checkpoints/deepseekmath/base'
save_mpath = r'/home/nachiketa/Documents/Workspaces/checkpoints/deepseekmath/gptq_int8'

model_name = base_path

#set the calibration dataset
calibration_dataset = load_dataset(
    "gsm8k", "main",
    #data_files="en/c4-train.00001-of-01024.json.gz",
    split="train"
  ).select(range(1024))["question"]


# quantization configuration
#quant_config = QuantizeConfig(bits=4, group_size=128)
quant_config = QuantizeConfig(bits=8, group_size=128)

# Create the modelcloud instance
model = GPTQModel.load(model_name, quant_config)

# increase `batch_size` to match gpu/vram specs to speed up quantization
model.quantize(calibration_dataset, batch_size=1)

# save the quantized model
model.save(save_mpath)