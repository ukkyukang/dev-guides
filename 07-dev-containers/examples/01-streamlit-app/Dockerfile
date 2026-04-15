# ============================================================
# 의존성이 설치된 이미지
# ============================================================
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# 1. 의존성 파일만 먼저 복사 (레이어 캐싱)
COPY pyproject.toml uv.lock ./

# 2. 의존성만 설치 (프로젝트 자체는 아직 설치 안 함)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# 3. 소스 복사 + 프로젝트 editable 설치
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# 개발 시에는 compose.dev.yml의 command가 이 CMD를 대체합니다
CMD ["uv", "run", "streamlit", "run", "src/my_app/app.py", "--server.address", "0.0.0.0"]
