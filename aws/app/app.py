import sys
import base64
import json
from fastapi import FastAPI
from mangum import Mangum
from llama_cpp import Llama

# Load the LLM, outside the handler so it persists between runs
llm = Llama(
   model_path="Llama-3.2-1B-Instruct-F16.gguf", # change if different model
   n_ctx=2048, # context length
   n_threads=6,  # maximum in AWS Lambda
)

# Creates a FastAPI app instance, which acts as an API server. This will handle incoming requests.
app = FastAPI()

# Defines a POST route (/chat). Accepts JSON payload (data: dict). The async function allows non-blocking execution (helpful for AI inference).
@app.post("/chat")
async def root(data: dict):
   # Calls an LLM function (llm()) for text generation.
   # Constructs a formatted prompt from the input_text field in the request.
   # Sets max_tokens=512, meaning the response will be limited to 512 tokens.
   # echo=True ensures that the original input is included in the response.
   output = llm(
       f"Instruct: {data['prompt']}\nOutput:",
       max_tokens=512,
       echo=True,
   )
   return {
       "statusCode": 200,
       "body": json.dumps(output)
   }

# Mangum acts as a middleware to convert FastAPI into an AWS Lambda-compatible format.
# This is necessary because AWS Lambda doesn’t directly support FastAPI, but Mangum bridges the gap.
handler = Mangum(app)