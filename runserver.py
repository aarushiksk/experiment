import uvicorn
from main import app  # Import the FastAPI app from main.py

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)