# fastapi-jinja-bootstrap-starter

## Quick start
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Open http://127.0.0.1:8000/ in your browser.

## Production image

Build the production image with compiled assets:
```bash
docker build -t <name> .
```

Run the container:
```bash
docker run -p 8000:8000 <name>
```

The production image bakes in frontend assets and does not require Node at runtime.
