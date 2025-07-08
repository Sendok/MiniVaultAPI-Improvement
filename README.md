# 🧠 MiniVault API – Full Feature Edition

A fully-local, production-grade REST API that simulates a core feature of ModelVault: receiving a prompt and returning a generated response. Now with true streaming, dynamic model loading, SQLite logging, rate limiting, and Docker support.

---

## 🚀 Features

- ✅ Real-time streaming using HuggingFace Transformers (`TextIteratorStreamer`)
- 🔁 `/generate` for full-text response
- 📤 `/generate/stream` for true token-by-token output
- 🔀 Dynamic model loader with automatic caching (`@lru_cache`)
- 🗃️ SQLite-based prompt-response logging (`db/minivault.db`)
- 🛡️ Rate limiting via `slowapi` (5 requests/minute per IP)
- 🖥️ CLI interface using `Typer`
- 🧪 Unit-tested via `pytest`
- 🐳 Dockerized for reproducibility

---

## 🛠️ Setup Instructions

### 1. Clone and Install

> ⚠️ Make sure you're using **Python 3.10+**

```bash
git clone https://github.com/Sendok/MiniVaultAPI-Improvement
cd MiniVaultAPI-Improvement
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Run the API Locally

```bash
uvicorn app.main:app --reload
```

Visit the API: [http://localhost:8000](http://localhost:8000)

---

## 🐳 Docker Instructions

### Build and Run with Docker:

```bash
docker build -t minivault .
docker run -p 8000:8000 minivault
```

> First run may download `distilgpt2` model via HuggingFace.

---

## 📦 API Endpoints

### `POST /generate`

Request:
```json
{ "prompt": "Hello world", "model": "distilgpt2" }
```

Response:
```json
{ "response": "Hello world, I am a language model..." }
```

---

### `POST /generate/stream`

Request:
```json
{ "prompt": "Once upon a time", "model": "distilgpt2" }
```

Response:  
Plain-text response streamed **token by token**. please Using CLI to see streamed **token by token**

curl -N -X POST http://localhost:8000/generate/stream -H "Content-Type: application/json" -d '{"prompt": "Once upon a time","model": "distilgpt2"}'


---

## 🖥️ CLI Tool

### Generate once:
```bash
python3 cli.py generate "Tell me a joke about LLMs"
```

### Stream output:
```bash
python3 cli.py stream "Write a short story"
```

---

## 🧪 Run Tests

```bash
pytest -v tests/test_main.py
```

---

## 🧠 Design Decisions & Improvements

- **True Token Streaming:** Implemented using `TextIteratorStreamer` for realistic generation.
- **Dynamic Model Loader:** Uses `AutoModelForCausalLM` and `AutoTokenizer`, with caching via `lru_cache`.
- **Rate Limiting:** Integrated `slowapi` to throttle request rate per IP.
- **SQLite Logging:** Prompts and responses stored in `interactions` table with timestamp.
- **Modular Design:** Clear separation between app logic, logging, streaming, and model handling.
- **CLI & Docker:** Simplifies testing and deployment in any environment.

---

## 💡 Future Work

- ✅ (Done) True real-time token streaming
- ✅ (Done) Switchable models with lazy loading
- ✅ (Done) SQLite-based structured logging
- ✅ (Done) Docker containerization
- 🔐 Add authentication for protected endpoints
- 📊 Add Prometheus/Grafana-compatible metrics exporter
- 🌐 Add Web UI (Gradio or Streamlit)

---

## 📂 Project Structure

```
minivault-api/
├── app/
│   ├── main.py              # FastAPI app
│   ├── models.py            # HuggingFace loader + cache
│   ├── streamer.py          # Streaming logic
│   ├── logger.py            # SQLite logging
│   ├── middlewares.py       # Rate limiter
│   └── schemas.py           # Request models
├── cli.py                   # Typer CLI
├── db/minivault.db          # SQLite DB
├── logs/log.jsonl           # (Optional) legacy logs
├── tests/test_api.py        # API test
├── Dockerfile
├── .dockerignore
├── requirements.txt
└── README.md
```

---

## 🙌 Acknowledgment

Built as part of the ModelVault take-home challenge.  
Fully offline. No cloud APIs are used.
