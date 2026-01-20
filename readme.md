# Backend Setup Instructions

This backend is built with FastAPI and uses `uv` for dependency management.

## Prerequisites

- Python 3.14 or higher
- `uv` installed (see [uv installation](https://github.com/astral-sh/uv))

## Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   uv venv
   ```

3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```
   uv sync
   ```

5. Set up environment variables:
   - Copy `.env.example` to `.env` and fill in the required values (if applicable).

6. Run database migrations (if using Tortoise ORM):
   ```
   aerich upgrade
   ```

7. Start the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`.

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.


# Frontend Setup Instructions

This frontend is built with Streamlit and uses `uv` for dependency management.

## Prerequisites

- Python 3.14 or higher
- `uv` installed (see [uv installation](https://github.com/astral-sh/uv))

## Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Create a virtual environment:
   ```
   uv venv
   ```

3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```
   uv sync
   ```

5. Set up environment variables:
   - Copy `.env.example` to `.env` and fill in the required values (if applicable).

6. Start the Streamlit app:
   ```
   streamlit run main.py
   ```

The app will be available at `http://localhost:8501`.

