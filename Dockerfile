FROM python:3.11-slim
WORKDIR /app
COPY road-guardin-agent/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY road-guardin-agent/ .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]