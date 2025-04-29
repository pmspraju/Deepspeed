# Stage 1: Build environment using a Python base image
FROM python:3.12 as builder

# Install build tools
RUN apt-get update && apt-get install -y gcc g++ cmake zip

# Copy requirements.txt and install packages with appropriate CMAKE_ARGS
COPY requirements.txt .
RUN CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" pip install --upgrade pip && pip install -r requirements.txt

FROM public.ecr.aws/lambda/python:3.12

# Install OpenMP library
RUN  dnf -y install libgomp

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /var/lang/lib/python3.12/site-packages/

# Copy lambda function code
COPY Llama-3.2-1B-Instruct-F16.gguf ${LAMBDA_TASK_ROOT}

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler
CMD [ "app.handler" ]