# ============================================================
# uv 기반 최적 Python Docker 이미지
# ============================================================
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# 바이트코드 컴파일 (시작 속도 향상)
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

# 1. 의존성 파일 먼저 복사 (캐싱)
COPY pyproject.toml uv.lock ./

# 2. 의존성 설치 (프로젝트 자체는 아직 설치하지 않음)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# 3. 소스코드 복사
COPY src/ ./src/

# 4. 프로젝트 설치
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
