# 07. 컨테이너 안에서 개발하기

> Docker 컨테이너 안에서 소스코드를 실행하며 개발하는 방법을 배웁니다.  
> 핵심 원리는 단순합니다: **이미지에 의존성을 굽고, 소스코드는 마운트한다.**


<!-- TOC -->
## 📑 목차

- [📋 사전 요구사항](#사전-요구사항)
- [🎯 학습 목표](#학습-목표)
- [📖 본문](#본문)
  - [1. 컨테이너 개발의 본질](#1-컨테이너-개발의-본질)
  - [2. 전체 흐름](#2-전체-흐름)
  - [3. 핵심 파일 3개](#3-핵심-파일-3개)
    - [3.1 `pyproject.toml` — 프로젝트 정의](#31-pyprojecttoml-프로젝트-정의)
    - [3.2 `Dockerfile` — 의존성이 설치된 이미지](#32-dockerfile-의존성이-설치된-이미지)
    - [3.3 `compose.dev.yml` — 소스 마운트 + 실행](#33-composedevyml-소스-마운트-실행)
  - [4. 개발 워크플로우](#4-개발-워크플로우)
    - [의존성을 추가해야 할 때](#의존성을-추가해야-할-때)
    - [컨테이너 안에서 직접 명령 실행](#컨테이너-안에서-직접-명령-실행)
  - [5. 왜 이렇게 하나? (vs 로컬 개발)](#5-왜-이렇게-하나-vs-로컬-개발)
- [❓ 자주 묻는 질문 (FAQ)](#자주-묻는-질문-faq)
  - [Q1: 소스코드 마운트하면 이미지 안의 코드와 충돌하지 않나요?](#q1-소스코드-마운트하면-이미지-안의-코드와-충돌하지-않나요)
  - [Q2: `uv sync`와 `uv pip install -e .`는 같은 건가요?](#q2-uv-sync와-uv-pip-install--e-는-같은-건가요)
  - [Q3: `--build` 없이 `up`만 하면?](#q3---build-없이-up만-하면)
  - [Q4: Windows에서도 되나요?](#q4-windows에서도-되나요)
- [🏗️ 예제 프로젝트](#예제-프로젝트)
- [🔗 참고 자료](#참고-자료)
- [⏭️ 다음 강의](#다음-강의)

<!-- /TOC -->

---

## 📋 사전 요구사항

- [05. Dockerfile](../05-dockerfile/README.md), [06. Docker Compose](../06-docker-compose/README.md) 강의 완료
- Docker 설치 및 실행

## 🎯 학습 목표

1. 컨테이너 개발의 핵심 원리를 이해한다
2. Dockerfile로 의존성이 설치된 이미지를 만든다
3. Docker Compose로 소스코드를 마운트하여 핫 리로드 개발 환경을 구성한다

---

## 📖 본문

### 1. 컨테이너 개발의 본질

컨테이너에서 개발한다는 것은, 이 두 가지를 분리하는 것입니다:

```
┌────────────────────────────────────────┐
│           Docker 이미지 (빌드)          │
│                                        │
│  Python, uv, 시스템 패키지             │
│  pip/uv로 설치한 라이브러리들           │
│  → 자주 변하지 않음 → 이미지에 굽는다   │
└────────────────────────────────────────┘
                    +
┌────────────────────────────────────────┐
│        소스코드 (볼륨 마운트)            │
│                                        │
│  내가 작성하는 코드 (src/)              │
│  → 수시로 변함 → 호스트에서 마운트한다   │
└────────────────────────────────────────┘
```

이 분리가 왜 중요한가요?

- **이미지 재빌드 없이** 코드를 수정하고 바로 반영됩니다
- **누구나 동일한 환경**에서 실행됩니다 (Python 버전, 라이브러리 버전)
- **로컬 PC를 오염시키지 않습니다** (Python, uv를 로컬에 설치할 필요 없음)

---

### 2. 전체 흐름

```
1. pyproject.toml 작성 (의존성 정의)
2. Dockerfile 작성 (의존성 설치 이미지)
3. compose.dev.yml 작성 (소스 마운트 + 실행)
4. docker compose -f compose.dev.yml up --build
5. 호스트에서 코드 수정 → 컨테이너에 즉시 반영!
```

---

### 3. 핵심 파일 3개

#### 3.1 `pyproject.toml` — 프로젝트 정의

```toml
[project]
name = "my-app"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "streamlit>=1.40.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/my_app"]
```

표준 uv 라이브러리 구조 (`--lib`)입니다. `src/my_app/` 안에 소스코드가 들어갑니다.

#### 3.2 `Dockerfile` — 의존성이 설치된 이미지

```dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# 의존성 파일만 먼저 복사 → 캐싱 최적화
COPY pyproject.toml uv.lock ./

# 의존성 설치 (프로젝트 자체는 아직 설치 안 함)
RUN uv sync --frozen --no-install-project

# 프로젝트를 editable 모드로 설치
# → src/my_app이 마운트되면 그 코드를 바로 사용
COPY . .
RUN uv sync --frozen
```

**핵심**: `uv sync`를 두 번 나눠서 실행합니다.
1. 첫 번째: 라이브러리만 설치 (캐시 활용)
2. 두 번째: 프로젝트 자체를 editable로 설치

#### 3.3 `compose.dev.yml` — 소스 마운트 + 실행

```yaml
services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./src:/app/src    # ← 핵심! 소스코드를 호스트에서 마운트
    command: uv run streamlit run src/my_app/app.py --server.address 0.0.0.0
```

**핵심**: `volumes: ./src:/app/src`
- 호스트의 `src/` 디렉토리가 컨테이너의 `/app/src`를 덮어씁니다
- 호스트에서 코드를 수정하면 컨테이너에 즉시 반영됩니다
- Streamlit은 기본적으로 파일 변경을 감지하여 자동 리로드합니다

---

### 4. 개발 워크플로우

```bash
# 처음 한 번만 (또는 의존성이 변경될 때만)
docker compose -f compose.dev.yml up --build

# 이후에는 빌드 없이
docker compose -f compose.dev.yml up

# 호스트에서 src/my_app/app.py를 수정하면
# → 컨테이너 안의 Streamlit이 자동으로 리로드됩니다!
```

#### 의존성을 추가해야 할 때

```bash
# 1. pyproject.toml에 의존성 추가 (호스트에서)
# 2. 이미지 재빌드
docker compose -f compose.dev.yml up --build
```

#### 컨테이너 안에서 직접 명령 실행

```bash
# 실행 중인 컨테이너에 접속
docker compose -f compose.dev.yml exec app bash

# 컨테이너 안에서 uv 명령어 사용
uv run python -c "import streamlit; print(streamlit.__version__)"
```

---

### 5. 왜 이렇게 하나? (vs 로컬 개발)

| | 로컬 개발 | 컨테이너 개발 |
|---|---|---|
| Python 설치 | 각자 로컬에 설치 | 이미지에 포함 ✅ |
| 라이브러리 버전 | 로컬 환경에 따라 다름 | 이미지에 고정 ✅ |
| "내 PC에서는 되는데" | 자주 발생 😫 | 불가능 ✅ |
| 새 팀원 온보딩 | Python, uv, 라이브러리 설치... | `docker compose up` 끝 ✅ |
| 로컬 환경 오염 | 프로젝트마다 Python 충돌 | 격리됨 ✅ |

---

## ❓ 자주 묻는 질문 (FAQ)

### Q1: 소스코드 마운트하면 이미지 안의 코드와 충돌하지 않나요?

**A**: `volumes`의 **마운트가 이미지의 파일을 덮어씁니다**. 그래서 이미지 빌드 시 `COPY . .`를 하지만, 런타임에는 호스트의 `src/`가 사용됩니다. editable 설치(`uv sync`)가 되어 있으므로 Python은 마운트된 소스를 참조합니다.

### Q2: `uv sync`와 `uv pip install -e .`는 같은 건가요?

**A**: 비슷하지만 `uv sync`가 더 권장됩니다. `uv sync`는 `uv.lock` 기반으로 결정론적 설치를 하고, editable 설치도 포함합니다. `uv pip install -e .`는 pip 호환 인터페이스로, lock 파일 없이 동작합니다.

### Q3: `--build` 없이 `up`만 하면?

**A**: 기존에 빌드된 이미지를 그대로 사용합니다. `pyproject.toml`이나 `Dockerfile`이 변경된 경우에만 `--build`를 추가하세요. 소스코드 변경은 마운트되므로 재빌드 불필요합니다.

### Q4: Windows에서도 되나요?

**A**: 네! Docker Desktop + WSL2 환경에서 동일하게 동작합니다. 단, 프로젝트를 WSL2 파일시스템(`~/projects/`)에 두어야 파일 마운트 성능이 좋습니다.

---

## 🏗️ 예제 프로젝트

| 예제 | 설명 |
|------|------|
| [01-streamlit-app](./examples/01-streamlit-app/) | Streamlit 앱을 컨테이너 안에서 개발하는 전체 예제 |

---

## 🔗 참고 자료

- [uv Docker 통합 가이드](https://docs.astral.sh/uv/guides/integration/docker/)
- [Streamlit 공식 문서](https://docs.streamlit.io/)
- [Dev Containers 공식 사양](https://containers.dev/) (VS Code 통합을 원한다면)

---

## ⏭️ 다음 강의

[08. Git — 초보자를 위한 실전 가이드 →](../08-git/README.md)
