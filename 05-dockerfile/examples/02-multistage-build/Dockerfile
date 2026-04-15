# ============================================================
# Stage 1: Builder
# ============================================================
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ============================================================
# Stage 2: Runtime (최소 이미지)
# ============================================================
FROM python:3.12-slim AS runtime

WORKDIR /app

# builder에서 설치된 패키지만 복사
COPY --from=builder /install /usr/local

COPY src/ ./src/

# 비루트 사용자
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
