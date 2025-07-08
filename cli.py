# Import Typer to build command-line interface
import typer
# Import requests to send HTTP requests to the API
import requests

# Create a Typer application instance
app = typer.Typer()

# Base URL of the FastAPI server
API_URL = "http://localhost:8000"

# Define a command to send a prompt and get a full response (non-streaming)
@app.command()
def generate(prompt: str, model: str = "distilgpt2"):
    # Send a POST request to the /generate endpoint with prompt and model
    res = requests.post(f"{API_URL}/generate", json={"prompt": prompt, "model": model})

    # Display the generated response in the terminal
    typer.echo(res.json()["response"])

# Define a command to stream the response token by token
@app.command()
def stream(prompt: str, model: str = "distilgpt2"):
    # Send a POST request to the /generate/stream endpoint and enable streaming
    with requests.post(f"{API_URL}/generate/stream", json={"prompt": prompt, "model": model}, stream=True) as r:
        # Iterate over streamed chunks
        for chunk in r.iter_content(chunk_size=None):
            if chunk:
                # Decode and print each chunk (without newline to simulate streaming)
                typer.echo(chunk.decode("utf-8"), nl=False)

# Run the CLI app if this script is executed directly
if __name__ == "__main__":
    app()
