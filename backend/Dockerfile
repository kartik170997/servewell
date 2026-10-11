FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends antiword && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.lock.txt .
RUN pip install --no-cache-dir -r requirements.lock.txt
COPY main.py .
RUN useradd -u 10001 -m folio && mkdir /data && chown folio:folio /data
USER folio
ENV DATA_DIR=/data
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
