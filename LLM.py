from transformers import pipeline, BitsAndBytesConfig, AutoModelForCausalLM, AutoTokenizer
from langchain_huggingface import HuggingFacePipeline
from template import template_mitigacion
import torch
import gc

gc.collect()
torch.cuda.empty_cache()

model_path = "Qwen/Qwen2.5-3B-Instruct"

# Cuantización 4-bit: reduce el modelo de ~6GB a ~2GB en VRAM
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    quantization_config=bnb_config,
    device_map="cuda:0",
)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    do_sample=False,        # greedy decoding: más rápido y consistente
    max_new_tokens=150,     # suficiente para una recomendación
    return_full_text=False
)

llm = HuggingFacePipeline(pipeline=pipe)
cadena_mitigacion = template_mitigacion | llm