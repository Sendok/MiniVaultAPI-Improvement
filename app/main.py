from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.middleware.cors import CORSMiddleware

from app.models import get_model
from app.streamer import stream_response
from app.logger import log_to_db, log_interaction
from app.middlewares import limiter  # limiter = Limiter(key_func=get_remote_address)

import asyncio

app = FastAPI()
app.state.limiter = limiter

# Rate limit error handler
app.add_exception_handler(
    RateLimitExceeded,
    lambda request, exc: JSONResponse(status_code=429, content={"error": "Too Many Requests"})
)

# CORS (opsional, sesuaikan jika ada frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str
    model: str = "distilgpt2"

@app.post("/generate")
@limiter.limit("5/minute")
async def generate(request: Request, payload: PromptRequest):
    model, tokenizer = get_model(payload.model)
    inputs = tokenizer(payload.prompt, return_tensors="pt")
    output = model.generate(**inputs, max_new_tokens=50)
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    log_to_db(payload.prompt, response)
    log_interaction(payload.prompt, response)

    return {"response": response}

@app.post("/generate/stream")
@limiter.limit("5/minute")
async def generate_stream(request: Request, payload: PromptRequest):
    model, tokenizer = get_model(payload.model)
    buffer = []

    async def streamer_wrapper():
        for token in stream_response(payload.prompt, model, tokenizer):
            buffer.append(token)
            yield token
            await asyncio.sleep(0.01)  # optional pacing

        # Log full response after streaming is complete
        full_response = "".join(buffer)
        log_to_db(payload.prompt, full_response)
        log_interaction(payload.prompt, full_response)

    return StreamingResponse(streamer_wrapper(), media_type="text/plain")
