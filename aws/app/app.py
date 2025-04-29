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

app = FastAPI()

def handler(event, context):
    print("Event is:", event)
    print("Context is:", context)

    # Locally the body is not encoded, via lambda URL it is
    try:
        if event.get('isBase64Encoded', False):
            body = base64.b64decode(event['body']).decode('utf-8')
        else:
            body = event['body']

        body_json = json.loads(body)
        prompt = body_json["prompt"]
    except (KeyError, json.JSONDecodeError) as e:
        return {"statusCode": 400, "body": f"Error processing request: {str(e)}"}

    output = llm(
        f"Instruct: {prompt}\nOutput:",
        max_tokens=512,
        echo=True,
    )

    return {
        "statusCode": 200,
        "body": json.dumps(output)
    }
