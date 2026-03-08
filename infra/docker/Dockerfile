FROM python:3.11-slim
WORKDIR /app
COPY backend /app/backend
COPY frontend/dist /app/frontend/dist
COPY data /app/data
COPY backend/pyproject.toml /app/backend/pyproject.toml
RUN pip install --no-cache-dir fastapi uvicorn[standard] sqlalchemy pydantic pydantic-settings python-multipart pillow
EXPOSE 8088
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8088"]
