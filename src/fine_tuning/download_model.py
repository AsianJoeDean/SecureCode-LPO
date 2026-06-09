import os
from dotenv import load_dotenv
from huggingface_hub import snapshot_download

# 1. Load your Hugging Face password from the hidden .env file
load_dotenv()
hf_token = os.getenv("HF_TOKEN")

def download_codellama():
    print("Connecting to Hugging Face...")
    
    # The exact name of the model on the website
    model_name = "meta-llama/CodeLlama-7b-hf"
    
    # 2. Start the download directly into your local models folder
    print(f"Downloading {model_name}. This is a massive file (~13GB), so grab a coffee...")
    
    snapshot_download(
        repo_id=model_name,
        local_dir="../../models/CodeLlama-7b",
        token=hf_token
    )
    
    print("Download complete! The AI model is successfully sitting in your /models folder.")

if __name__ == "__main__":
    download_codellama()