# Import classes to load pre-trained language models and tokenizers
from transformers import AutoModelForCausalLM, AutoTokenizer

# Import caching decorator to avoid reloading models repeatedly
from functools import lru_cache

# Load and cache a language model and its tokenizer by name
@lru_cache(maxsize=4)  # Cache up to 4 different models to reduce loading time
def get_model(name: str):
    # Load tokenizer from Hugging Face
    tokenizer = AutoTokenizer.from_pretrained(name)
    
    # Load the causal language model (e.g., GPT-style)
    model = AutoModelForCausalLM.from_pretrained(name)
    
    # Set the model to evaluation mode (disable dropout, etc.)
    model.eval()

    # Return both the model and tokenizer
    return model, tokenizer
