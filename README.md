# Deepspeed
try deepspeed with pytorch

# VLLM
try vllm in Lambda AI gpu instance

---

```markdown
# 🧠 LLM Deployment Journey: AWS Lambda → SageMaker → GPU Inference with vLLM

This guide documents an end-to-end AI deployment pipeline explored in real-world development: from serverless AWS Lambda functions and SageMaker debugging, to full vLLM inference running on Lambda GPU Cloud with Dockerized DeepSeek 7B models.

---

## 🪐 Part 1: AWS Lambda Functions

> Automate model workflows or data orchestration using serverless Lambda functions.

### ✅ Highlights
- Used Lambda to trigger SageMaker jobs and S3 processes
- Attached IAM execution role with policies for:
  - Accessing S3 buckets
  - Initiating SageMaker actions
- Debugged a key-based SSH authentication error (`Permission denied (publickey)`)
  - Determined it was unrelated to Lambda — traced to local scp/SSH issues fixed later

---

## 🧩 Part 2: AWS SageMaker Deployment

> Deployed DeepSeek 7B model using DeepSpeed on a DJL container with SageMaker

### ✅ Steps
- Configured IAM:
  - Attached S3 read access to execution role
  - Verified trust relationships for SageMaker
- Structured model archive:
  ```
  model.tar.gz/
  ├── model.py
  ├── config.json
  ├── tokenizer.json
  └── pytorch_model.bin
  ```
- Uploaded model to S3 and created `HuggingFaceModel` using SageMaker Python SDK
- Used appropriate container URI (DJL DeepSpeed)
- Debugged endpoint failures and container logs
  - Fixed `ModelError`, permission denials, and environment mismatches

---

## ⚙️ Part 3: Lambda GPU + vLLM Inference Server

> Run DeepSeek 7B inside a CUDA 12.8 Docker container with vLLM for local or remote API access

### 📁 Folder Structure

```
vllm-server/
└── app/
    ├── Dockerfile
    ├── requirements.txt
    ├── start.sh
    └── deepseek-math-7b/
```

---

### 🛠️ Build Docker Image

```bash
# From inside app/
sudo docker build -t vllm-cuda128 .
```

- Re-ran build if PyPI downloads failed
- Used `sudo` for Docker access on new instance
- Optional: pinned `xformers` or added retry logic

---

### 🚀 Run Container

```bash
sudo docker run --gpus all -p 8000:8000 \
  -v $(pwd)/deepseek-math-7b:/models \
  -e MODEL_PATH=/models \
  vllm-cuda128
```

- Mounts model directory into container at `/models`
- Starts vLLM API server on `0.0.0.0:8000`

---

### 🧪 Test Inference from Instance

```bash
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "/models",
    "prompt": "Explain the chain rule",
    "max_tokens": 64
  }'
```

- Verified model ID by hitting:
  ```
  curl http://localhost:8000/v1/models
  ```
- Used returned `"id": "/models"` as model name

---

### 🌐 Enable Browser & Remote Access

1. Go to Lambda Cloud firewall
2. Open TCP port 8000
3. Access via browser:
   ```
   http://<your-ip>:8000/v1/models
   ```

---

### 📦 Export & Transfer Docker Image

On instance:
```bash
sudo docker save vllm-cuda128 -o vllmDs7b.tar
sudo chown ubuntu:ubuntu vllmDs7b.tar
```

From local machine:
```bash
scp -i ~/Keys/L1A100.pem \
  ubuntu@<ip>:/home/ubuntu/vllm-server/app/vllmDs7b.tar \
  ~/Downloads/
```

Load into local Docker:
```bash
docker load -i ~/Downloads/vllmDs7b.tar
```

---

## 🧠 Summary

| Capability            | What You Implemented                                        |
|----------------------|-------------------------------------------------------------|
| 🚀 Serverless         | Lambda function triggering SageMaker/S3 securely           |
| 🧰 Cloud inference    | SageMaker + DeepSpeed containerization                      |
| 🐳 Portable runtime   | CUDA 12.8 Docker with vLLM + DeepSeek                       |
| 🌍 API integration    | Browser-accessible OpenAI-style API from Lambda GPU        |
| 🛫 Image transfer     | Docker save/load + secure scp download                      |

---
