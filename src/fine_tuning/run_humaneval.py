import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from human_eval.data import write_jsonl, read_problems
from tqdm import tqdm
import re

# 1. Load your newly secured model in 4-bit
model_path = "./secure_codellama_merged"
print(f"Loading {model_path}...")

tokenizer = AutoTokenizer.from_pretrained(model_path)
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)
model = AutoModelForCausalLM.from_pretrained(
    model_path, 
    device_map="auto", 
    quantization_config=quant_config
)

# 2. Load the HumanEval dataset
problems = read_problems()
task_ids = list(problems.keys()) # THE FIX: Load all 164 puzzles

samples = []
print(f"\nStarting HumanEval Code Generation (All {len(task_ids)} Puzzles)...")
print("This will take a little while. Let the GPU cook!")

for task_id in tqdm(task_ids):
    prompt = problems[task_id]["prompt"]
    
    # Instruct models perform best when given their specific instruction tags
    formatted_prompt = f"[INST] Complete the following Python code:\n{prompt} [/INST]"
    
    inputs = tokenizer(formatted_prompt, return_tensors="pt").to("cuda")
    
    # Generate the code with a low temperature (0.2)
    outputs = model.generate(
        **inputs, 
        max_new_tokens=256,
        temperature=0.2,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )
    
    input_length = inputs['input_ids'].shape[1]
    generated_text = tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)
    
    # 3. Extract ONLY the code inside the markdown blocks
    ticks = "`" * 3
    pattern = f"{ticks}(?:python)?(.*?){ticks}"
    match = re.search(pattern, generated_text, re.DOTALL | re.IGNORECASE)
    
    if match:
        clean_code = match.group(1).strip()
    else:
        clean_code = generated_text.strip()
        
    samples.append(dict(task_id=task_id, completion=clean_code))

# 4. Save the results
output_file = "humaneval_merged_samples.jsonl"
write_jsonl(output_file, samples)

print(f"\n✅ Generation Complete! Saved {len(samples)} completions to {output_file}.")