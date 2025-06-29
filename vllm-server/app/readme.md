## Try Vllm in Lambda AI gpu
#### Used A100 40GB Pcle GPU instance for Deepseek-7b-math model.

### Docker commands

#### Initial docker commands 
```
sudo systemctl restart docker
docker images -f dangling=true
docker rmi <image id>
docker image prune
```

#### Give perminssion for the key
```
chmod 400 /home/nachiketa/Documents/Keys/lambda/L1A100.pem
```

#### Login in to the labmda instance
```
ssh -i /home/nachiketa/Documents/Keys/lambda/L1A100.pem ubuntu@104.171.202.210
```

#### Upload the project and model. This should NOT be inside instance shell
#### Should be in normal terminal as long as paths exists
```
scp -i /home/nachiketa/Documents/Keys/lambda/L1A100.pem -r /home/nachiketa/Documents/Workspaces/Deepspeed/vllm-server ubuntu@104.171.202.210:~/
```

#### Get in to the folder having docker files and issue build command
```
cd vllm-server/app
sudo docker build -t vllm-cuda128 .
```

#### allow the ubuntu user to access the Docker socket
#### Then logout and log back in (or reboot) for the change to take effect. After that, you can run Docker commands directly without sudo
```
sudo usermod -aG docker $USER
newgrp docker
```

#### To clean up any partial builds/cache before retrying.
```
sudo docker system prune -f
```

#### If our folder structure of project is like below
```
vllm-server/
└── app/
    ├── Dockerfile
    ├── requirements.txt
    ├── start.sh
    └── deepseek-math-7b/
```

### Navigate to the folder inside lambda instance
```
cd vllm-server/app
```

#### Docker run
```
sudo docker run --gpus all -p 8000:8000 \
  -v $(pwd)/deepseek-math-7b:/models \
  -e MODEL_PATH=/models \
  vllm-cuda128
```

#### See the mounted model card 
```
curl http://localhost:8000/v1/models
Result - 
{"id":"cmpl-2e5e681fd75942e093acfbe7ab72f886",
 "object":"text_completion",
 "created":7141,
 "model":"/models",
 "choices":[{"index":0,"text":" Mainly, you take the derivative of y'' taken with respect to x. Section 7-2 : Proof of Various Derivative Properties.\nThose included the legend. The mathematical theory of differentiation was stated for the first time by Isaac Newton in De Analysi, but Leibniz independently put together the fundamentals of","logprobs":null,"finish_reason":"length"}],
 "usage":{"prompt_tokens":8,"total_tokens":72,"completion_tokens":64}
}
```

#### Use the value in "model" in the test command
```
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "/models",
    "prompt": "Explain the chain rule in calculus.",
    "max_tokens": 64
  }'
Result - 
{"id":"cmpl-2e5e681fd75942e093acfbe7ab72f886",
 "object":"text_completion",
 "created":7141,
 "model":"/models",
 "choices":[{"index":0,
             "text":" Mainly, you take the derivative of y'' taken with respect to x. Section 7-2 : Proof of Various Derivative Properties.
           \nThose included the legend. The mathematical theory of differentiation was stated for the first time by Isaac Newton in De Analysi, but Leibniz independently put together the fundamentals of",
           "logprobs":null,
           "finish_reason":"length"}],
 "usage":{"prompt_tokens":8,"total_tokens":72,"completion_tokens":64}}ubuntu@104-171-202-210:~$ curl http://localhost:8000/
```

#### Step1: To build if yml fil exists: Navigate to the app folder and build the docker image. Ensure .yml file is present.
```
docker compose up --build
```

#### see the running containers inside the instance
```
sudo docker ps -a
Output - 
CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS                      PORTS                                         NAMES
cb284ebcf1aa   vllm-cuda128   "/opt/nvidia/nvidia_…"   24 minutes ago   Up 24 minutes               0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp   pedantic_elion
dcade48047e2   vllm-cuda128   "/opt/nvidia/nvidia_…"   46 minutes ago   Exited (1) 46 minutes ago                                                 upbeat_gagarin
```

#### see the docker logs, real time logs
```
sudo docker logs cb284ebcf1aa
sudo docker logs -f cb284ebcf1aa
```

#### To enter the container's shell
```
sudo docker exec -it cb284ebcf1aa /bin/sh
```

#### Save the docker image to a tar file
```
sudo docker save -o vllmDs7b.tar vllm-cuda128
```
#### Give permssion of the tar file to ubuntu uer
```
sudo chown ubuntu:ubuntu /home/ubuntu/vllm-server/app/vllmDs7b.tar
```

#### Download the image to your local machine
```
scp -i /home/nachiketa/Documents/Keys/lambda/L1A100.pem \
    ubuntu@104.171.202.210:/home/ubuntu/vllm-server/app/vllmDs7b.tar \
    /home/nachiketa/Documents/Workspaces/Dockerimages/vllm-deepseek-7b-base/
```

#### to stop the continaer
```
Ctr + c
```