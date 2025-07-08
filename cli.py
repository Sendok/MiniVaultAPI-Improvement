import typer
import requests

app = typer.Typer()

API_URL = "http://localhost:8000"

@app.command()
def generate(prompt: str, model: str = "distilgpt2"):
    res = requests.post(f"{API_URL}/generate", json={"prompt": prompt, "model": model})
    typer.echo(res.json()["response"])

@app.command()
def stream(prompt: str, model: str = "distilgpt2"):
    with requests.post(f"{API_URL}/generate/stream", json={"prompt": prompt, "model": model}, stream=True) as r:
        for chunk in r.iter_content(chunk_size=None):
            if chunk:
                typer.echo(chunk.decode("utf-8"), nl=False)

if __name__ == "__main__":
    app()
