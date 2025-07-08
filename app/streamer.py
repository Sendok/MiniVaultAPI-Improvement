from transformers import TextIteratorStreamer
import threading

def stream_response(prompt, model, tokenizer):
    inputs = tokenizer(prompt, return_tensors="pt")
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

    generation_kwargs = dict(**inputs, streamer=streamer, max_new_tokens=50)

    thread = threading.Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()

    for token in streamer:
        if token.strip():  # hindari token kosong
            yield token
