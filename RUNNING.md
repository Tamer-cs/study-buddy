# Run instructions

1. Create a virtual environment and activate it (Windows):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Start the development server:

```powershell
uvicorn src.app.main:app --reload --port 8000
```

4. Health check: GET http://127.0.0.1:8000/health
