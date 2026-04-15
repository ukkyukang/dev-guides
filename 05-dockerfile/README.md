# 05. Dockerfile

> 효율적이고 안전한 Docker 이미지를 빌드하기 위한 Dockerfile 작성법을 배웁니다.  
> 레이어 캐싱, 멀티스테이지 빌드, uv 통합까지 실무 패턴을 다룹니다.

---

## 📋 사전 요구사항

- [04. WSL과 Docker & Docker Registry](../04-wsl-docker-registry/README.md) 강의 완료
- Docker 설치 및 기본 명령어 이해
- [01. uv](../01-uv/README.md) 기본 사용법

## 🎯 학습 목표

1. Dockerfile의 주요 명령어를 이해하고 올바르게 사용할 수 있다
2. 레이어 캐싱 전략으로 빌드 시간을 단축할 수 있다
3. 멀티스테이지 빌드로 이미지 크기를 최소화할 수 있다
4. uv를 활용한 최적의 Python Docker 이미지를 빌드할 수 있다
5. 보안 모범 사례를 적용할 수 있다

---

## 📖 본문

### 1. Dockerfile 기초

Dockerfile은 Docker 이미지를 빌드하기 위한 **레시피 파일**입니다.

#### 1.1 기본 구조

```dockerfile
# 1. 베이스 이미지
FROM python:3.12-slim

# 2. 메타데이터
LABEL maintainer="dev@company.com"
LABEL version="1.0.0"

# 3. 작업 디렉토리 설정
WORKDIR /app

# 4. 파일 복사
COPY requirements.txt .

# 5. 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 6. 소스코드 복사
COPY . .

# 7. 포트 노출 (문서화 목적)
EXPOSE 8000

# 8. 실행 명령
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 1.2 주요 명령어 레퍼런스

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `FROM` | 베이스 이미지 지정 | `FROM python:3.12-slim` |
| `WORKDIR` | 작업 디렉토리 설정 | `WORKDIR /app` |
| `COPY` | 파일/디렉토리 복사 | `COPY . .` |
| `ADD` | COPY + URL 다운로드 + 압축 해제 | `ADD app.tar.gz /app` |
| `RUN` | 빌드 시 명령어 실행 | `RUN pip install flask` |
| `CMD` | 컨테이너 시작 시 기본 명령 | `CMD ["python", "app.py"]` |
| `ENTRYPOINT` | 컨테이너 시작 시 고정 명령 | `ENTRYPOINT ["python"]` |
| `ENV` | 환경 변수 설정 | `ENV PYTHONDONTWRITEBYTECODE=1` |
| `ARG` | 빌드 시 전달 변수 | `ARG PYTHON_VERSION=3.12` |
| `EXPOSE` | 포트 문서화 | `EXPOSE 8000` |
| `VOLUME` | 볼륨 마운트 포인트 | `VOLUME /data` |
| `USER` | 실행 사용자 변경 | `USER appuser` |

#### 1.3 `CMD` vs `ENTRYPOINT`

```dockerfile
# CMD만 사용 — 실행 시 완전히 덮어쓸 수 있음
CMD ["python", "app.py"]
# docker run my-image                → python app.py
# docker run my-image bash           → bash (CMD 대체됨)

# ENTRYPOINT만 사용 — 항상 실행됨
ENTRYPOINT ["python"]
# docker run my-image                → python
# docker run my-image app.py         → python app.py (인수 추가)

# 조합 사용 (권장) — ENTRYPOINT는 고정, CMD는 기본 인수
ENTRYPOINT ["python"]
CMD ["app.py"]
# docker run my-image                → python app.py
# docker run my-image test.py        → python test.py (CMD만 대체)
```

---

### 2. 베이스 이미지 선택

#### 2.1 Python 베이스 이미지 비교

| 이미지 | 크기 | 특징 | 추천 상황 |
|--------|------|------|----------|
| `python:3.12` | ~1GB | Debian 기반, 빌드 도구 포함 | C 확장 빌드 필요 시 |
| `python:3.12-slim` | ~150MB | Debian 최소 설치 | 🏆 **대부분의 경우** |
| `python:3.12-alpine` | ~50MB | Alpine Linux 기반 | 이미지 크기가 최우선 |
| `python:3.12-bookworm` | ~1GB | Debian Bookworm | 특정 Debian 버전 필요 |

#### 2.2 Alpine 주의사항

```dockerfile
# ⚠️ Alpine은 musl libc를 사용하여 일부 패키지 호환 문제 발생
# numpy, pandas 등 C 확장 패키지의 빌드 시간이 매우 길어질 수 있음

# 권장: slim 이미지 사용
FROM python:3.12-slim
```

#### 2.3 uv 공식 이미지

```dockerfile
# uv가 사전 설치된 공식 이미지 (권장 ✅)
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
```

---

### 3. 레이어 캐싱 전략

Docker는 Dockerfile의 각 명령어를 별도의 **레이어**로 저장합니다. 변경되지 않은 레이어는 캐시를 재사용합니다.

#### 3.1 캐싱 규칙

1. 한 레이어가 변경되면 그 이후 **모든 레이어**가 무효화됨
2. `COPY` 명령어는 파일 내용의 변경을 감지
3. 자주 변경되는 것은 **뒤쪽에** 배치

#### 3.2 ❌ 비효율적인 순서

```dockerfile
FROM python:3.12-slim
WORKDIR /app

# ❌ 소스코드 먼저 복사 → 코드 한 줄만 바꿔도 pip install 재실행
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
```

#### 3.3 ✅ 최적화된 순서

```dockerfile
FROM python:3.12-slim
WORKDIR /app

# ✅ 의존성 파일만 먼저 복사
COPY requirements.txt .

# ✅ 의존성 설치 (requirements.txt가 안 바뀌면 캐시 사용!)
RUN pip install --no-cache-dir -r requirements.txt

# ✅ 소스코드는 나중에 복사
COPY . .

CMD ["python", "app.py"]
```

---

### 4. 멀티스테이지 빌드

빌드에 필요한 도구(컴파일러, 빌드 도구 등)를 최종 이미지에 포함하지 않는 기법입니다.

#### 4.1 기본 패턴

```dockerfile
# ============================================================
# Stage 1: Builder — 빌드 도구 + 의존성 설치
# ============================================================
FROM python:3.12-slim AS builder

WORKDIR /app

# 빌드 도구 설치 (C 확장 컴파일에 필요)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ============================================================
# Stage 2: Runtime — 최소한의 실행 환경
# ============================================================
FROM python:3.12-slim AS runtime

WORKDIR /app

# builder에서 설치된 패키지만 복사
COPY --from=builder /install /usr/local

# 소스코드 복사
COPY . .

# 비루트 사용자로 실행
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**결과**: 빌드 도구가 제외되어 최종 이미지 크기가 대폭 감소.

---

### 5. uv를 활용한 Python Docker 이미지 (권장 ✅)

#### 5.1 uv 공식 이미지 활용

```dockerfile
# ============================================================
# uv 기반 최적 Python Docker 이미지
# ============================================================
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# 바이트코드 컴파일 활성화 (컨테이너 시작 속도 향상)
ENV UV_COMPILE_BYTECODE=1

# uv 캐시를 빌드 캐시로 활용
ENV UV_LINK_MODE=copy

WORKDIR /app

# 1. 의존성 파일만 먼저 복사 (캐싱 최적화)
COPY pyproject.toml uv.lock ./

# 2. 의존성 설치 (--frozen: lock 파일 기반, --no-dev: 개발 의존성 제외)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# 3. 소스코드 복사
COPY . .

# 4. 프로젝트 자체 설치
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# 5. 실행
CMD ["uv", "run", "python", "-m", "app"]
```

#### 5.2 멀티스테이지 + uv

```dockerfile
# ============================================================
# Stage 1: 의존성 설치
# ============================================================
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ============================================================
# Stage 2: 최소 실행 이미지 (uv 미포함)
# ============================================================
FROM python:3.12-slim AS runtime

WORKDIR /app

# builder에서 가상환경만 복사
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

# 가상환경의 Python을 PATH에 추가
ENV PATH="/app/.venv/bin:$PATH"

# 비루트 사용자
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### 6. `.dockerignore`

빌드 컨텍스트에서 불필요한 파일을 제외합니다:

```dockerignore
# 버전 관리
.git
.gitignore

# Python
__pycache__
*.pyc
*.pyo
.venv
*.egg-info
dist
build

# IDE
.vscode
.idea
*.swp

# Docker
Dockerfile*
docker-compose*.yml
compose*.yml

# 기타
.env
*.md
tests/
docs/
```

---

### 7. 보안 모범 사례

```dockerfile
# 1. 비루트 사용자로 실행
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# 2. 불필요한 패키지 설치 금지
RUN apt-get update && apt-get install -y --no-install-recommends \
    필요한패키지만 \
    && rm -rf /var/lib/apt/lists/*

# 3. 시크릿을 이미지에 포함하지 마세요
# ❌ ENV SECRET_KEY=my-secret
# ✅ 런타임에 환경변수로 주입: docker run -e SECRET_KEY=my-secret

# 4. COPY 대신 ADD 사용 자제 (보안상 COPY가 안전)

# 5. 특정 버전 고정 (latest 태그 사용 금지)
# ❌ FROM python:latest
# ✅ FROM python:3.12-slim
```

---

### 8. 디버깅 팁

```bash
# 빌드 과정 상세 로그
docker build --progress=plain -t my-app .

# 특정 스테이지까지만 빌드
docker build --target builder -t my-app:builder .

# 빌드된 이미지의 레이어 확인
docker history my-app

# 이미지 크기 상세 확인
docker inspect my-app | jq '.[0].Size'

# 실패한 빌드의 중간 레이어에서 디버깅
docker run -it --rm my-app:builder bash
```

---

## ❓ 자주 묻는 질문 (FAQ)

### Q1: `COPY . .` 에서 `.`은 무엇인가요?

**A**: 첫 번째 `.`은 빌드 컨텍스트(보통 Dockerfile이 있는 디렉토리)의 현재 위치, 두 번째 `.`은 컨테이너의 `WORKDIR`입니다.

### Q2: `RUN` 명령어를 왜 `&&`로 연결하나요?

**A**: 각 `RUN`은 별도의 레이어를 생성합니다. 연결하면 레이어 수를 줄이고 중간 파일(apt 캐시 등)을 같은 레이어에서 정리할 수 있습니다.

```dockerfile
# ❌ 3개 레이어 (apt 캐시가 레이어에 남음)
RUN apt-get update
RUN apt-get install -y git
RUN rm -rf /var/lib/apt/lists/*

# ✅ 1개 레이어
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*
```

### Q3: `--mount=type=cache`는 무엇인가요?

**A**: BuildKit의 빌드 캐시 마운트입니다. 패키지 다운로드 캐시를 빌드 간에 공유하여 반복 빌드 속도를 향상시킵니다. 최종 이미지에는 포함되지 않습니다.

### Q4: Alpine과 slim 중 어떤 것을 써야 하나요?

**A**: **대부분 `slim`을 사용하세요.** Alpine은 musl libc를 사용하여 numpy, pandas 등의 C 확장 패키지에서 호환 문제와 긴 빌드 시간이 발생합니다. 50MB의 이미지 크기 차이보다 안정성이 더 중요합니다.

### Q5: 이미지 빌드 시 `--no-cache-dir`를 왜 쓰나요?

**A**: pip의 다운로드 캐시를 저장하지 않아 이미지 크기를 줄입니다. Docker 레이어에 불필요한 캐시 파일이 포함되는 것을 방지합니다.

---

## 🏗️ 예제 프로젝트

| 예제 | 설명 | 핵심 학습 |
|------|------|----------|
| [01-basic-image](./examples/01-basic-image/) | 기본 Dockerfile | FROM, COPY, RUN, CMD |
| [02-multistage-build](./examples/02-multistage-build/) | 멀티스테이지 빌드 | builder/runtime 분리 |
| [03-uv-docker](./examples/03-uv-docker/) | uv 기반 Docker 이미지 | uv sync, 캐시 최적화 |

---

## 🔗 참고 자료

- [Dockerfile 레퍼런스](https://docs.docker.com/reference/dockerfile/)
- [Docker 빌드 모범 사례](https://docs.docker.com/build/building/best-practices/)
- [uv Docker 통합 가이드](https://docs.astral.sh/uv/guides/integration/docker/)

---

## ⏭️ 다음 강의

[06. Docker Compose →](../06-docker-compose/README.md)
