# Almanack Backend

FastAPI backend server for the Almanack application.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Available Endpoints

- `GET /` - Health check
- `GET /health` - Health check
- `GET /api/hello` - Simple hello message
- `GET /api/messages` - Get all messages
- `POST /api/message` - Create a new message

## Development

The server runs on port 8000 and is configured with CORS to allow requests from the Next.js frontend running on port 3000. 