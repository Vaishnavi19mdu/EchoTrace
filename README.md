# projwhitehat

Backend service for detecting Human vs AI-generated voices.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

3. Add your API keys to `.env`:
- `API_KEY`: Your custom API key for protecting the endpoint
- `GEMINI_API_KEY`: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Running the Server
```bash
# Development
python -m app.main

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Server runs at: `http://localhost:8000`

## API Usage

### Endpoint: `POST /analyze`

**Headers:**