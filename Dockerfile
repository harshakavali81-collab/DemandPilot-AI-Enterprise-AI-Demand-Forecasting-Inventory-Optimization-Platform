FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .
COPY dashboard ./dashboard
COPY scripts ./scripts
COPY docs ./docs
COPY artifacts ./artifacts
COPY data ./data
EXPOSE 8000
CMD ["uvicorn","demandpilot.api.main:app","--host","0.0.0.0","--port","8000"]
