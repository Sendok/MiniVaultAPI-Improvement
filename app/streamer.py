# Import Hugging Face's streaming utility for text generation
from transformers import TextIteratorStreamer
# Import threading to run model generation in a separate thread
import threading

# Function to stream generated tokens one by one
def stream_response(prompt, model, tokenizer):
    # Tokenize the input prompt and return as PyTorch tensors
    inputs = tokenizer(prompt, return_tensors="pt")

    # Create a streamer to yield tokens as they are generated
    # skip_prompt=True ensures only generated output is streamed
    # skip_special_tokens=True omits tokens like <EOS>
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

    # Prepare arguments for the model's generate function
    generation_kwargs = dict(**inputs, streamer=streamer, max_new_tokens=50)

    # Run model.generate in a background thread so we can stream output in real-time
    thread = threading.Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()

    # Yield tokens as they become available from the streamer
    for token in streamer:
        if token.strip():  # Skip empty or whitespace-only tokens
            yield token
