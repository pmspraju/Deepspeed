# Docker commands
# To build if yml fil exists
## docker compose up --build

# see the running containers
## docker ps
## output
```
CONTAINER ID   IMAGE        COMMAND                  CREATED          STATUS          PORTS                                         NAMES
118aba493f1b   llm-lambda   "/lambda-entrypoint.…"   19 minutes ago   Up 19 minutes   0.0.0.0:9000->8080/tcp, [::]:9000->8080/tcp   app-llm-lambda-1
```

# test the aws lambda container but via http request
## curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'

# test if it is rest api
## curl -X POST http://localhost:9000 -H "Content-Type: application/json" -d '{"input": "Hello"}'

# docker logs
## docker logs app-llm-lambda-1

# docker real time logs
## docker logs -f llm-lambda

# To enter the container's shell
## docker exec -it llm-lambda /bin/sh

## Ctr + c to stop the continaer

# AWS Commands

## aws configure list 
## aws s3 ls s3://nasanex/

```
export AWS_REGION=us-east-1
aws ecr create-repository --repository-name llm-lambda --region $AWS_REGION
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
docker tag llm-lambda:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/llm-lambda:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/llm-lambda:latest
export LAMBDA_ROLE_NAME="lambda_cli"
export IAM_POLICY_FILE="trust-policy.json"
export LAMBDA_ROLE_ARN=$(aws iam get-role --role-name $LAMBDA_ROLE_NAME --query 'Role.Arn' --output text)

aws iam list-attached-role-policies --role-name 'lambda_cli'
aws iam list-attached-role-policies --role-name 'lambda_cli'
```