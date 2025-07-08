# Import FastAPI core functionality
from fastapi import FastAPI, Request
# Import response classes for normal and streaming responses
from fastapi.responses import StreamingResponse, JSONResponse
# Import Pydantic for request validation
from pydantic import BaseModel
# Import rate limiting tools from SlowAPI
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
# Import CORS middleware to allow cross-origin requests
from starlette.middleware.cors import CORSMiddleware

# Import custom modules for model loading, streaming, and logging
from app.models import get_model
from app.streamer import stream_response
from app.logger import log_to_db, log_interaction
from app.middlewares import limiter  # limiter = Limiter(key_func=get_remote_address)

import asyncio  # Used for async delay in streaming

# Create FastAPI app instance
app = FastAPI()
# Attach the rate limiter to app state
app.state.limiter = limiter

# Register handler for rate limit exceeded errors (HTTP 429)
app.add_exception_handler(
    RateLimitExceeded,
    lambda request, exc: JSONResponse(status_code=429, content={"error": "Too Many Requests"})
)

# Enable CORS (allows frontend from any origin to access the API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Allow all origins (you can restrict in production)
    allow_credentials=True,
    allow_methods=["*"],           # Allow all HTTP methods
    allow_headers=["*"],           # Allow all headers
)

# Define the expected request body structure for both endpoints
class PromptRequest(BaseModel):
    prompt: str                   # User input prompt
    model: str = "distilgpt2"     # Optional model name, default to distilgpt2

# Synchronous text generation endpoint
@app.post("/generate")
@limiter.limit("5/minute")        # Limit each client to 5 requests per minute
async def generate(request: Request, payload: PromptRequest):
    # Load the specified model and tokenizer
    model, tokenizer = get_model(payload.model)
    
    # Tokenize the input prompt
    inputs = tokenizer(payload.prompt, return_tensors="pt")
    
    # Generate output using the model (up to 50 new tokens)
    output = model.generate(**inputs, max_new_tokens=50)
    
    # Decode model output into human-readable text
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    # Log the prompt and response to the database and interaction log
    log_to_db(payload.prompt, response)
    log_interaction(payload.prompt, response)

    # Return the final response as JSON
    return {"response": response}

# Streaming version of the generation endpoint
@app.post("/generate/stream")
@limiter.limit("5/minute")        # Same rate limit
async def generate_stream(request: Request, payload: PromptRequest):
    # Load the model and tokenizer
    model, tokenizer = get_model(payload.model)
    buffer = []  # To store streamed tokens for logging after completion

    # Define async generator that yields tokens one by one
    async def streamer_wrapper():
        for token in stream_response(payload.prompt, model, tokenizer):
            buffer.append(token)         # Save token for final log
            yield token                  # Stream token to client
            await asyncio.sleep(0.01)    # Optional delay for smoother output

        # After streaming is finished, log the full response
        full_response = "".join(buffer)
        log_to_db(payload.prompt, full_response)
        log_interaction(payload.prompt, full_response)

    # Return the streaming response as plain text
    return StreamingResponse(streamer_wrapper(), media_type="text/plain")
