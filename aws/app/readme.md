## Docker commands
## To build if yml fil exists

### Step1: Navigate to the app folder and build the docker image. Ensure .yml file is present.
```
docker compose up --build
```

## see the running containers
### docker ps
### output
```
CONTAINER ID   IMAGE        COMMAND                  CREATED          STATUS          PORTS                                         NAMES
118aba493f1b   llm-lambda   "/lambda-entrypoint.…"   19 minutes ago   Up 19 minutes   0.0.0.0:9000->8080/tcp, [::]:9000->8080/tcp   app-llm-lambda-1
```

### Step2: test the aws lambda container but via http request
```
curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```

### test if it is rest api
```
curl -X POST http://localhost:9000 -H "Content-Type: application/json" -d '{"input": "Hello"}'
```

## see the docker logs, real time logs
```
docker logs app-llm-lambda-1
docker logs -f llm-lambda
```

## To enter the container's shell
```
docker exec -it llm-lambda /bin/sh
```

### Ctr + c to stop the continaer

## AWS Commands

### aws configure list 
### aws s3 ls s3://nasanex/

### List the policies attached to a role
```
aws iam list-attached-role-policies --role-name 'lambda_cli'
aws iam list-attached-role-policies --role-name 'lambda_cli'
```

### Step3: Create a ECR repository
```
export AWS_REGION=us-east-1
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
aws ecr create-repository --repository-name llm-lambda --region $AWS_REGION
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
```

### Step4: Create a tag and push the docker image to the ecr repository
```
docker tag llm-lambda:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/llm-lambda:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/llm-lambda:latest
```

### Step5: Get the lambda role arn.
```
export LAMBDA_ROLE_NAME="lambda_cli"
export IAM_POLICY_FILE="trust-policy.json"
export LAMBDA_ROLE_ARN=$(aws iam get-role --role-name $LAMBDA_ROLE_NAME --query 'Role.Arn' --output text)
```

### Step6:
### Used aws console to create a lambda function for the image we pushed
### Get the lambda function arn 
```
export AWS_REGION=us-east-1
export LAMBDA_FUNCTION_NAME="llma-lambda"
export FUNCTION_URL=$(aws lambda get-function-url-config --region $AWS_REGION --function-name $LAMBDA_FUNCTION_NAME --query 'FunctionUrl' --output text)
```

### Step7: 
### Do the inference using the lambda function if NO fastapi
```
export PROMPT="Generate a good name for a bakery."
curl $FUNCTION_URL \
    -d '{ "body": "{ \"prompt\": \"$PROMPT\" }" }' \
    | jq -r '.choices[0].text, .usage'
```

### Do the inference using the lambda function if NO fastapi
### Mangum converts API Gateway requests into FastAPI requests internally. 
### FastAPI routes like @app.post("/chat") expect direct JSON input, not an API Gateway event structure. 
### Removing resource, path, requestContext makes it a clean FastAPI request.
```
export PROMPT="How to learn LLM."
curl -X POST "$FUNCTION_URL/chat" \
  -H "Content-Type: application/json" \
  -d "{\"prompt\": \"$PROMPT\"}"
```

