
from djl_python import Input, Output
import os
import deepspeed
import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

predictor = None


def get_model(properties):
    model_name = "s3://deepseek-math-7b/"
    tensor_parallel = properties["tensor_parallel_degree"]
    local_rank = int(os.getenv("LOCAL_RANK", "0"))
    model = AutoModelForCausalLM.from_pretrained(
        model_name, revision="float32", torch_dtype=torch.float32
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    model = deepspeed.init_inference(
        model,
        mp_size=tensor_parallel,
        dtype=model.dtype,
        replace_method="auto",
        replace_with_kernel_inject=True,
    )
    generator = pipeline(
        task="text-generation", model=model, tokenizer=tokenizer, device=local_rank
    )
    return generator


def handle(inputs: Input) -> None:
    global predictor
    if not predictor:
        predictor = get_model(inputs.get_properties())

    if inputs.is_empty():
        # Model server makes an empty call to warmup the model on startup
        return None

    data = inputs.get_as_string()
    result = predictor(data, do_sample=True, max_new_tokens=256)
    return Output().add(result)
