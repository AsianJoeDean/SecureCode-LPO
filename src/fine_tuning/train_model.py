import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from datasets import load_dataset
from trl import DPOTrainer, DPOConfig
from peft import LoraConfig

def train_secure_model():
    # 1. Load the Formatted Data
    print("Loading LPO dataset...")
    dataset = load_dataset('json', data_files='data/lpo_dataset.json', split='train')

    # 2. Set up QLoRA (The "Shrink Ray" to fit the AI on your laptop)
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16
    )

    # 3. Load the AI Model and Tokenizer
    model_path = "meta-llama/CodeLlama-13b-Instruct-hf"
    print("Loading base model into local memory...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        quantization_config=quantization_config,
        device_map="auto" # Automatically handles your GPU memory
    )

    # 4. Set the Training Rules (The "Red Pen")
    training_args = DPOConfig(
        output_dir="./secure_codellama",
        per_device_train_batch_size=1, 
        max_steps=50,
        learning_rate=2e-4,
        fp16=True,   # Tell the GPU to use standard 16-bit math
        bf16=False   # Explicitly disable the unsupported Brain Float math
    )

    # 5. Define the trainable adapters (The "Sticky Notes")
    peft_config = LoraConfig(
        r=8,
        lora_alpha=16,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "v_proj"] # Targets the attention layers in LLaMA
    )

    # 6. Initialize the Trainer
    trainer = DPOTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        tokenizer=tokenizer, 
        peft_config=peft_config,    # Attached the LoRA configuration
    )

    # 7. Start the Training
    print("Starting Localized Preference Optimization...")
    trainer.train()

    # 8. Save the Adapters to the hard drive!
    trainer.save_model("./secure_codellama")

if __name__ == "__main__":
    train_secure_model()