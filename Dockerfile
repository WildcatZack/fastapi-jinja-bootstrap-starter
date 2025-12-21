# Multi-stage build for production runtime
FROM node:20-alpine AS builder

WORKDIR /build/frontend

# Ensure backend static directory exists for build outputs
RUN mkdir -p /build/app/static

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ .
RUN npm run build

FROM python:3.12-slim AS runtime

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app
COPY --from=builder /build/app/static ./app/static

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
