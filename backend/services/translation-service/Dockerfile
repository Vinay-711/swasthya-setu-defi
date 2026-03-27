FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5002
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:5002/health || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5002"]
