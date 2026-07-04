import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from human_eval.data import write_jsonl, read_problems
from tqdm import tqdm
import re

# 1. Load the original BASELINE model in 4-bit
model_path = "meta-llama/CodeLlama-13b-Instruct-hf"
print(f"Loading BASELINE model: {model_path}...")

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
task_ids = list(problems.keys())

samples = []
print(f"\nStarting Baseline HumanEval Generation (All {len(task_ids)} Puzzles)...")
print("Time to let the GPU cook one last time!")

for task_id in tqdm(task_ids):
    prompt = problems[task_id]["prompt"]
    
    formatted_prompt = f"[INST] Complete the following Python code:\n{prompt} [/INST]"
    
    inputs = tokenizer(formatted_prompt, return_tensors="pt").to("cuda")
    
    outputs = model.generate(
        **inputs, 
        max_new_tokens=256,
        temperature=0.2,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )
    
    input_length = inputs['input_ids'].shape[1]
    generated_text = tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)
    
    # 3. Extract the markdown
    ticks = "`" * 3
    pattern = f"{ticks}(?:python)?(.*?){ticks}"
    match = re.search(pattern, generated_text, re.DOTALL | re.IGNORECASE)
    code = match.group(1).strip() if match else generated_text.strip()
        
    # 4. Clean the Indentation / Duplicate Signatures instantly
    cleaned_lines = []
    in_def = False
    for l in code.split("\n"):
        if in_def:
            cleaned_lines.append(l)
        elif l.startswith("def "):
            in_def = True
            
    final_code = "\n".join(cleaned_lines) if cleaned_lines else code
    samples.append(dict(task_id=task_id, completion=final_code))

# 5. Save the perfectly formatted results
output_file = "humaneval_baseline_samples.jsonl"
write_jsonl(output_file, samples)

print(f"\n✅ Generation Complete! Saved {len(samples)} completions to {output_file}.")