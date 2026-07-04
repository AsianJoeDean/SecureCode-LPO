import json
import os

def format_for_lpo():
    input_file = "data/full_dataset.json"
    output_file = "data/lpo_dataset.json"
    
    # 1. Ensure your Phase 1 dataset actually exists
    if not os.path.exists(input_file):
        print(f"Error: Could not find {input_file}. Run generate_data.py first.")
        return

    print("Reading Phase 1 dataset...")
    with open(input_file, "r") as file:
        dataset = json.load(file)
        
    lpo_formatted_data = []
    
    # 2. Reformat each entry for the Hugging Face DPOTrainer
    for entry in dataset:
        vuln_type = entry.get("vulnerability_type", "vulnerability")
        
        # Build a realistic instruction prompt for the AI to read during training
        prompt = f"Write a secure Python function. Ensure it is protected against {vuln_type}.\n\nCode:"
        
        # Map your generated code to the exact keys Hugging Face requires
        lpo_entry = {
            "prompt": prompt,
            "chosen": entry.get("good_code", ""),
            "rejected": entry.get("bad_code", "")
        }
        lpo_formatted_data.append(lpo_entry)
        
    # 3. Save the new, LPO-ready dataset
    with open(output_file, "w") as file:
        json.dump(lpo_formatted_data, file, indent=4)
        
    print(f"Success! Formatted {len(lpo_formatted_data)} examples.")
    print(f"Ready for Phase 3. Saved to: {output_file}")

if __name__ == "__main__":
    format_for_lpo()