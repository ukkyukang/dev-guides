FROM python:3.12-slim

WORKDIR /app

# 의존성 파일 먼저 복사 (캐싱 최적화)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스코드 복사
COPY src/ ./src/

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
