import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI

# Load the secret API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_full_dataset(num_examples=10):
    print(f"Starting generation of {num_examples} code pairs...")
    
    dataset = []
    
    # 1. A list of different attacks to keep the training data diverse
    vuln_types = [
        "SQL Injection", 
        "Cross-Site Scripting (XSS)", 
        "Command Injection", 
        "Path Traversal", 
        "Hardcoded Credentials"
    ]

    # 2. Loop the API call
    for i in range(num_examples):
        # Pick the next vulnerability type from the list
        current_vuln = vuln_types[i % len(vuln_types)]
        print(f"Generating example {i+1}/{num_examples}: {current_vuln}...")
        
        prompt = f"""
        Write a realistic Python function that contains a {current_vuln} vulnerability. 
        Then, provide the patched, secure version of that function. 
        Finally, briefly explain why the original was vulnerable.
        Format your response perfectly as JSON with these exact keys: "bad_code", "good_code", "explanation".
        """

        try:
            # Call the GPT-4o API
            response = client.chat.completions.create(
                model="gpt-4o",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert. Always output valid JSON."},
                    {"role": "user", "content": prompt}
                ]
            )

            # Convert the text response into a real Python dictionary
            output_dict = json.loads(response.choices[0].message.content)
            
            # Tag the entry with the attack type so it's organized
            output_dict["vulnerability_type"] = current_vuln
            dataset.append(output_dict)
            
            # 3. Pause for a second to avoid hitting OpenAI API speed limits
            time.sleep(1)

        except Exception as e:
            print(f"Error on example {i+1}: {e}")

    # 4. Save the massive list to a single master file
    os.makedirs("../../data", exist_ok=True)
    file_path = "../../data/full_dataset.json"
    
    with open(file_path, "w") as file:
        json.dump(dataset, file, indent=4) # indent=4 makes the JSON readable for humans
        
    print(f"Done! Saved {len(dataset)} examples to {file_path}")

if __name__ == "__main__":
    # Start by generating 10 examples just to test that the loop works perfectly.
    # Once it works, change this to 100 or 500!
    generate_full_dataset(10)