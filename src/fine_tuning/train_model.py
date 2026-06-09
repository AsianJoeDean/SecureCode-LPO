import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

def load_model_for_training():
    print("Configuring QLoRA memory-saving settings...")
    
    # 1. Set up the 4-bit compression (This is the magic that saves your RAM/VRAM)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    
    # 2. Point to the massive model you just downloaded locally
    model_path = "../../models/CodeLlama-7b"
    
    print(f"Loading CodeLlama from local folder: {model_path}")
    print("This might take a minute...")
    
    # Load the tokenizer (how the AI reads text)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    # Fix for padding issues in Llama models
    tokenizer.pad_token = tokenizer.eos_token 

    # Load the actual AI model using the 4-bit compression config
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        quantization_config=bnb_config,
        device_map="auto" # Automatically splits the workload between your GPU and CPU
    )
    
    # 3. Prepare the model for training
    model = prepare_model_for_kbit_training(model)
    
    # 4. Set up the LoRA adapters (We only train ~1% of the model's brain to save time/memory)
    lora_config = LoraConfig(
        r=8, 
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"], # Target the attention mechanisms
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    
    model = get_peft_model(model, lora_config)
    
    print("\n✅ Success! The model is loaded and ready for fine-tuning.")
    
    # Print out how many parameters we are actually updating (It should be tiny!)
    model.print_trainable_parameters()
    
    return model, tokenizer

if __name__ == "__main__":
    # Test loading the model without crashing!
    model, tokenizer = load_model_for_training()