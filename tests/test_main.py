from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

def test_generate_stubbed_response():
    prompt = "Hello world"
    response = client.post("/generate", json={"prompt": prompt})
    assert response.status_code == 200
    json_data = response.json()
    assert "response" in json_data
    assert prompt in json_data["response"]

def test_generate_streaming_response():
    prompt = "Once upon a time"
    response = client.post("/generate/stream", json={"prompt": prompt})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")

    content = ""
    for chunk in response.iter_text():
        content += chunk

    # Pastikan ada output, bukan kosong
    assert len(content.strip()) > 0
    # Bisa juga periksa panjang minimal respons
    assert len(content.split()) >= 3



def test_log_file_written():
    assert os.path.exists("logs/log.jsonl")
    with open("logs/log.jsonl") as f:
        lines = f.readlines()
    assert len(lines) > 0

