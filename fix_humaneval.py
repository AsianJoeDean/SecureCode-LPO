import json

fixed_samples = []

with open("humaneval_merged_samples.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        sample = json.loads(line)
        code = sample["completion"]
        
        cleaned_lines = []
        in_def = False
        
        # Sift through the AI's answer line by line
        for l in code.split("\n"):
            if in_def:
                cleaned_lines.append(l)
            elif l.startswith("def "):
                in_def = True # We found the signature, start saving everything AFTER this!
                
        # If the AI didn't rewrite the 'def' signature, use its original answer
        if not cleaned_lines:
            final_code = code
        else:
            final_code = "\n".join(cleaned_lines)
            
        fixed_samples.append({"task_id": sample["task_id"], "completion": final_code})

# Save the perfectly formatted logic to a new file
with open("humaneval_merged_samples_fixed.jsonl", "w", encoding="utf-8") as f:
    for sample in fixed_samples:
        f.write(json.dumps(sample) + "\n")

print("\n✅ Cleaned 164 puzzles! Saved to humaneval_merged_samples_fixed.jsonl")