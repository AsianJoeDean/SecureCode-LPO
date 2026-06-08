import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load the secret API key from the hidden .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_practice_data():
    print("Asking GPT-4o for vulnerable and secure code...")
    
    # 2. Set up the multi-turn conversational prompt
    prompt = """
    Write a simple Python function that contains a SQL Injection vulnerability. 
    Then, provide the patched, secure version of that function. 
    Finally, briefly explain why the original was vulnerable.
    Format your response perfectly as JSON with these exact keys: "bad_code", "good_code", "explanation".
    """

    # 3. Call the GPT-4o API
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={ "type": "json_object" }, # Forces the AI to return clean data, not a chatty paragraph
        messages=[
            {"role": "system", "content": "You are a cybersecurity expert. Always output valid JSON."},
            {"role": "user", "content": prompt}
        ]
    )

    # 4. Extract the JSON response
    output_text = response.choices[0].message.content
    
    # 5. Make sure the 'data' folder actually exists, then save the file
    os.makedirs("../../data", exist_ok=True)
    file_path = "../../data/sample_sql_injection.json"
    
    with open(file_path, "w") as file:
        file.write(output_text)
        
    print(f"Done! Saved the AI practice data to {file_path}")

if __name__ == "__main__":
    generate_practice_data()