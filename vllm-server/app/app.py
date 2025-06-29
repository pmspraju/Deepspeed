# references
# https://horosin.com/deploy-a-language-model-llm-on-aws-lambda

import sys
import base64
import json
from fastapi import FastAPI
from mangum import Mangum
from llama_cpp import Llama
import torch

print("torch vesion:{}", torch.__version__)