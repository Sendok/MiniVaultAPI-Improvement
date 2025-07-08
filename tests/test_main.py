# Import FastAPI test client to simulate API calls
from fastapi.testclient import TestClient
# Import the FastAPI app instance
from app.main import app
import os  # For checking log file existence

# Initialize the test client with the app
client = TestClient(app)

# Test the /generate endpoint for a valid response
def test_generate_stubbed_response():
    prompt = "Hello world"
    # Send a POST request to /generate
    response = client.post("/generate", json={"prompt": prompt})
    
    # Ensure the response was successful
    assert response.status_code == 200

    # Parse the response JSON
    json_data = response.json()

    # Make sure the response contains a "response" key
    assert "response" in json_data

    # Check that the prompt appears in the generated output
    assert prompt in json_data["response"]

# Test the /generate/stream endpoint for valid streaming output
def test_generate_streaming_response():
    prompt = "Once upon a time"
    # Send a POST request to /generate/stream
    response = client.post("/generate/stream", json={"prompt": prompt})

    # Ensure the response was successful
    assert response.status_code == 200

    # Check that the content type is streaming text
    assert response.headers["content-type"].startswith("text/plain")

    content = ""
    # Collect streamed tokens from the response
    for chunk in response.iter_text():
        content += chunk

    # Ensure the response is not empty
    assert len(content.strip()) > 0

    # Optionally check for a minimum number of words
    assert len(content.split()) >= 3

# Test that the JSON log file is being written
def test_log_file_written():
    # Check that the log file exists
    assert os.path.exists("logs/log.jsonl")
    
    # Open the log file and read lines
    with open("logs/log.jsonl") as f:
        lines = f.readlines()
    
    # Ensure at least one log entry exists
    assert len(lines) > 0
