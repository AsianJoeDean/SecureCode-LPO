import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load the secret API key and force the terminal to read the fresh .env file
load_dotenv(override=True)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_full_dataset(num_examples=8):
    print(f"Starting generation of {num_examples} secure/insecure code pairs...")
    dataset = []
    
    # 2. Rotate through different attack types
    vuln_types = [
        "SQL Injection", 
        "Command Injection", 
        "Path Traversal",
        "Hardcoded Credentials"
    ]

    for i in range(num_examples):
        current_vuln = vuln_types[i % len(vuln_types)]
        print(f"Generating example {i+1}/{num_examples}: {current_vuln}...")
        
        prompt = f"""
        Write a realistic Python function that contains a {current_vuln} vulnerability. 
        Then, provide the patched, secure version of that function. 
        Finally, briefly explain why the original was vulnerable.
        Format your response perfectly as JSON with exact keys: "bad_code", "good_code", "explanation".
        """

        try:
            # 3. Using gpt-4o-mini to keep the project costs basically at zero
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert. Always output valid JSON."},
                    {"role": "user", "content": prompt}
                ]
            )

            output_dict = json.loads(response.choices[0].message.content)
            output_dict["vulnerability_type"] = current_vuln
            dataset.append(output_dict)
            
            # Pause to avoid hitting API speed limits
            time.sleep(1)

        except Exception as e:
            print(f"Error on example {i+1}: {e}")

    # 4. Save the file directly to your project's data folder (Fixed Path!)
    os.makedirs("data", exist_ok=True)
    file_path = "data/full_dataset.json"
    
    with open(file_path, "w") as file:
        json.dump(dataset, file, indent=4)
        
    print(f"Done! Saved {len(dataset)} examples to {file_path}")

if __name__ == "__main__":
    # Bumping the volume up to 100 to build the production-ready dataset!
    generate_full_dataset(100)