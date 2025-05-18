## Point to the model locally

```
export MODEL_PATH=/home/nachiketa/Documents/Workspaces/checkpoints/deepseekmath/base
```

## Create a s3 bucket 
```
aws s3api create-bucket --bucket deepseek-math-7b --region us-east-1
```

## Copy model to the s3 bucket as a folder recursively. 
```
aws s3 cp $MODEL_PATH s3://deepseek-math-7b/ --recursive
```

## Create a role and policies 
