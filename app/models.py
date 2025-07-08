from transformers import AutoModelForCausalLM, AutoTokenizer
from functools import lru_cache

@lru_cache(maxsize=4)
def get_model(name: str):
    tokenizer = AutoTokenizer.from_pretrained(name)
    model = AutoModelForCausalLM.from_pretrained(name)
    model.eval()
    return model, tokenizer
