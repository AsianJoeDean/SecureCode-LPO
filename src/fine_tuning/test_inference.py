import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

# 1. Paths
base_model_path = "meta-llama/CodeLlama-13b-Instruct-hf"
adapter_path = "./secure_codellama"

print("Loading base model in 4-bit...")
tokenizer = AutoTokenizer.from_pretrained(base_model_path)

# 2. The Missing Link: Re-enable 4-bit Quantization
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4"
)

# 3. Load Model with Quantization
model = AutoModelForCausalLM.from_pretrained(
    base_model_path, 
    device_map="auto", 
    quantization_config=quant_config,
)

print("Attaching secure adapters...")
# 4. Attach your new "Security" adapters
model = PeftModel.from_pretrained(model, adapter_path)

# 5. Test with a prompt that usually leads to insecure code
prompt = "Write a Python function to connect to a SQL database and execute a query."
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

print("\n--- AI Response ---")
outputs = model.generate(**inputs, max_new_tokens=200)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))