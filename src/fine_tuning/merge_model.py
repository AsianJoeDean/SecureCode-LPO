import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

base_model_path = "meta-llama/CodeLlama-13b-Instruct-hf"
adapter_path = "./secure_codellama"
output_path = "./secure_codellama_merged"

print("1. Loading base model (bypassing Python memory managers)...")
tokenizer = AutoTokenizer.from_pretrained(base_model_path)
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_path,
    low_cpu_mem_usage=True,
    return_dict=True,
    torch_dtype=torch.float16
    # device_map has been completely removed!
)

print("2. Attaching the security adapters...")
model = PeftModel.from_pretrained(base_model, adapter_path)

print("3. Fusing weights! This will take a few minutes using OS virtual memory...")
model = model.merge_and_unload()

print(f"4. Saving the unified deployment artifact to {output_path}...")
model.save_pretrained(output_path, safe_serialization=True)
tokenizer.save_pretrained(output_path)

print("Merge complete! Your model is ready for deployment.")