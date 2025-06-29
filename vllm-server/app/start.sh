#!/bin/bash
set -e

# Use local model path or fallback to HF model
MODEL_PATH=${MODEL_PATH:-"/models"}

echo "🔹 Starting vLLM server with model: $MODEL_PATH"

python3 -m vllm.entrypoints.openai.api_server \
  --model $MODEL_PATH \
  --dtype float16 \
  --max-model-len 2048 \
  --port 8000 \
  --tensor-parallel-size 1
