# 01. uv — 차세대 Python 패키지 매니저

> Rust로 작성된 초고속 Python 패키지 및 프로젝트 관리 도구를 배웁니다.  
> `pip`, `pip-tools`, `pipx`, `poetry`, `pyenv`, `virtualenv`를 **하나의 도구**로 대체할 수 있습니다.

---

## 📋 사전 요구사항

- 터미널(쉘) 기본 사용법
- Python 기초 문법 이해 (패키지, 모듈 개념)
- **Python 사전 설치 불필요** — uv가 Python 버전 관리까지 수행합니다

## 🎯 학습 목표

이 강의를 완료하면 다음을 할 수 있습니다:

1. `uv`를 설치하고 기본 명령어를 사용할 수 있다
2. `uv`로 Python 버전을 관리할 수 있다
3. `uv`로 프로젝트를 생성하고 의존성을 관리할 수 있다
4. `uv workspace`를 사용하여 모노레포를 구성할 수 있다
5. 사설 PyPI 인덱스와 연동할 수 있다
6. 기존 `pip`/`poetry` 프로젝트를 `uv`로 마이그레이션할 수 있다

---

## 📖 본문

### 1. uv란?

[uv](https://github.com/astral-sh/uv)는 [Astral](https://astral.sh/) 사에서 개발한 **Rust 기반 Python 패키지 관리자**입니다. 2024년 초에 출시되어 빠르게 Python 생태계의 표준 도구로 자리 잡고 있습니다.

#### 왜 uv를 사용해야 하는가?

| 기존 도구 | uv가 대체하는 기능 |
|-----------|-------------------|
| `pip`, `pip-tools` | 패키지 설치, 의존성 잠금 |
| `poetry`, `pdm` | 프로젝트 관리, 빌드, 배포 |
| `pyenv` | Python 버전 관리 |
| `virtualenv`, `venv` | 가상 환경 생성 및 관리 |
| `pipx` | CLI 도구 실행 및 설치 |

#### 핵심 장점

- **⚡ 초고속 성능**: Rust로 작성되어 `pip` 대비 10~100배 빠른 패키지 설치
- **🔒 결정론적 빌드**: `uv.lock` 파일로 크로스 플랫폼 재현 가능한 환경 보장
- **🐍 Python 버전 관리 내장**: `pyenv` 없이 Python 설치 및 전환
- **📦 올인원**: 하나의 바이너리로 프로젝트 생성부터 배포까지
- **🔄 호환성**: 기존 `pip` 명령어와 호환되는 인터페이스 제공
- **💾 글로벌 캐시**: 디스크 공간을 절약하는 효율적 캐싱 시스템

---

### 2. 설치

#### macOS / Linux

```bash
# 공식 설치 스크립트 (권장)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Homebrew (macOS)
brew install uv
```

#### Windows

```powershell
# 공식 설치 스크립트 (권장)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# winget
winget install --id=astral-sh.uv -e

# scoop
scoop install uv
```

#### 설치 확인

```bash
uv --version
# uv 0.7.x (예시)
```

#### 셸 자동완성 설정

```bash
# Bash
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc

# Zsh
echo 'eval "$(uv generate-shell-completion zsh)"' >> ~/.zshrc

# Fish
uv generate-shell-completion fish | source

# PowerShell
Add-Content -Path $PROFILE -Value '(& uv generate-shell-completion powershell) | Out-String | Invoke-Expression'
```

---

### 3. Python 버전 관리

uv는 Python 버전 설치 및 관리를 내장하고 있어, `pyenv`가 더 이상 필요하지 않습니다.

#### 사용 가능한 Python 버전 확인

```bash
uv python list
```

#### Python 설치

```bash
# 특정 버전 설치
uv python install 3.12

# 여러 버전 동시 설치
uv python install 3.11 3.12 3.13

# 최신 버전 설치
uv python install
```

#### 기본 Python 버전 고정

```bash
# 현재 디렉토리에 .python-version 파일 생성
uv python pin 3.12
```

`.python-version` 파일이 생성되며, `uv run`이나 `uv sync` 시 자동으로 해당 버전을 사용합니다.

#### Python 버전으로 직접 실행

```bash
# 특정 Python 버전으로 스크립트 실행
uv run --python 3.12 python script.py
```

---

### 4. 프로젝트 생성 및 관리

#### 4.1 새 프로젝트 생성

```bash
# 애플리케이션 프로젝트 생성 (기본값)
uv init my-project
cd my-project

# 라이브러리 프로젝트 생성 (패키지 배포 목적)
uv init --lib my-library
```

#### 생성된 프로젝트 구조

**애플리케이션 프로젝트** (`uv init my-project`):

```
my-project/
├── .python-version      # Python 버전 고정
├── README.md
├── pyproject.toml        # 프로젝트 메타데이터 및 의존성
└── main.py               # 진입점
```

**라이브러리 프로젝트** (`uv init --lib my-library`):

```
my-library/
├── .python-version
├── README.md
├── pyproject.toml
└── src/
    └── my_library/
        ├── __init__.py
        └── py.typed        # 타입 힌트 지원 마커
```

#### 4.2 `pyproject.toml` 이해하기

`pyproject.toml`은 프로젝트의 **단일 진실 소스(Single Source of Truth)** 입니다:

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "프로젝트 설명"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "httpx>=0.27.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "ruff>=0.8.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**주요 섹션 설명:**

| 섹션 | 설명 |
|------|------|
| `[project]` | 프로젝트 이름, 버전, Python 버전 요구사항, 의존성 |
| `[project.optional-dependencies]` | 선택적 의존성 그룹 (개발, 테스트 등) |
| `[build-system]` | 빌드 백엔드 설정 |
| `[tool.uv]` | uv 전용 설정 (소스, 인덱스 등) |

#### 4.3 의존성 관리

```bash
# 의존성 추가
uv add fastapi
uv add "httpx>=0.27.0"          # 버전 범위 지정
uv add ruff --dev                # 개발 의존성으로 추가
uv add pytest --group test       # 특정 그룹에 추가

# 의존성 제거
uv remove fastapi

# 의존성 동기화 (uv.lock 기반으로 설치)
uv sync

# 개발 의존성 포함 동기화
uv sync --all-groups

# 특정 그룹만 동기화
uv sync --group test

# 의존성 트리 확인
uv tree
```

#### 4.4 `uv.lock` 파일

`uv add` 또는 `uv sync` 실행 시 자동으로 생성/업데이트되는 **잠금 파일**입니다.

- **크로스 플랫폼**: 하나의 lock 파일이 모든 OS에서 동작
- **결정론적**: 동일한 lock 파일은 항상 동일한 환경을 생성
- **Git에 커밋**: 팀원 모두가 동일한 환경을 사용하도록 반드시 커밋

```bash
# lock 파일만 업데이트 (설치하지 않음)
uv lock

# 특정 패키지만 업그레이드
uv lock --upgrade-package fastapi

# 모든 패키지 업그레이드
uv lock --upgrade
```

> ⚠️ **주의**: `uv.lock` 파일을 직접 수정하지 마세요. 항상 `uv add`, `uv remove`, `uv lock` 명령어를 사용하세요.

#### 4.5 스크립트 실행

```bash
# 프로젝트 환경에서 Python 실행
uv run python main.py

# 프로젝트 환경에서 모듈 실행
uv run -m pytest

# 프로젝트의 스크립트 엔트리포인트 실행
uv run my-cli-tool
```

`uv run`은 실행 전에 자동으로:
1. 가상 환경이 없으면 생성
2. 의존성이 동기화되지 않았으면 동기화
3. 그 후 명령어 실행

---

### 5. 가상 환경

uv는 프로젝트 루트에 `.venv/` 디렉토리로 가상 환경을 자동 관리합니다.

```bash
# 가상 환경 직접 생성 (보통 자동 생성되므로 필요 없음)
uv venv

# 특정 Python 버전으로 가상 환경 생성
uv venv --python 3.12

# 가상 환경 활성화 (직접 사용 시)
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows
```

> 💡 **팁**: `uv run` 명령어를 사용하면 가상 환경을 직접 활성화할 필요가 없습니다. `uv run`이 자동으로 가상 환경 안에서 실행해줍니다.

---

### 6. CLI 도구 관리

uv는 `pipx`를 대체하여 Python CLI 도구를 관리할 수 있습니다.

```bash
# 도구를 설치하지 않고 일회성 실행
uvx ruff check .
uvx black --check .

# 도구 전역 설치
uv tool install ruff
uv tool install black

# 설치된 도구 목록
uv tool list

# 도구 업그레이드
uv tool upgrade ruff
uv tool upgrade --all
```

> 💡 `uvx`는 `uv tool run`의 단축 명령어입니다.

---

### 7. Workspace (모노레포)

여러 패키지를 하나의 저장소에서 관리해야 할 때 **workspace**를 사용합니다.

#### 7.1 Workspace 구조

```
my-monorepo/
├── pyproject.toml              # 워크스페이스 루트
├── uv.lock                     # 전체 워크스페이스 공용 Lock 파일
├── packages/
│   ├── core/
│   │   ├── pyproject.toml      # 공통 라이브러리
│   │   └── src/core/
│   ├── api/
│   │   ├── pyproject.toml      # API 서버
│   │   └── src/api/
│   └── cli/
│       ├── pyproject.toml      # CLI 도구
│       └── src/cli/
```

#### 7.2 루트 `pyproject.toml` 설정

```toml
[project]
name = "my-monorepo"
version = "0.1.0"
requires-python = ">=3.12"

[tool.uv.workspace]
members = ["packages/*"]
```

#### 7.3 멤버 패키지에서 다른 멤버 참조

```toml
# packages/api/pyproject.toml
[project]
name = "api"
version = "0.1.0"
dependencies = [
    "core",          # 같은 워크스페이스의 패키지를 이름으로 참조
    "fastapi>=0.115.0",
]

[tool.uv.sources]
core = { workspace = true }    # 워크스페이스 소스 명시
```

#### 7.4 Workspace 핵심 특징

- **단일 Lock 파일**: 모든 멤버가 하나의 `uv.lock`을 공유
- **단일 가상 환경**: 루트의 `.venv`를 모든 멤버가 공유
- **자동 에디터블 설치**: 멤버 패키지는 자동으로 editable 모드로 설치
- **독립 빌드**: 각 멤버는 독립적으로 빌드 및 배포 가능

```bash
# 특정 멤버 패키지에서 명령 실행
uv run --package api python -m api

# 특정 멤버의 의존성만 동기화
uv sync --package api
```

---

### 8. 사설 PyPI 인덱스 연동

회사 내부 패키지를 사설 인덱스에서 설치해야 하는 경우:

#### 8.1 `pyproject.toml`에서 인덱스 설정

```toml
[tool.uv]
index-url = "https://pypi.company.com/simple/"

# 또는 추가 인덱스 사용
[[tool.uv.index]]
name = "company"
url = "https://pypi.company.com/simple/"

# 특정 패키지를 특정 인덱스에서 가져오기
[tool.uv.sources]
company-sdk = { index = "company" }
```

#### 8.2 인증 설정

인증이 필요한 사설 인덱스의 경우, 환경 변수를 사용합니다:

```bash
# 환경 변수로 인증 정보 설정
export UV_INDEX_COMPANY_USERNAME="user"
export UV_INDEX_COMPANY_PASSWORD="token"

# 또는 URL에 직접 포함 (CI/CD 환경에서 주로 사용)
# 보안에 주의하세요!
```

`~/.config/uv/uv.toml` (전역 설정)에서도 설정 가능합니다:

```toml
[[index]]
name = "company"
url = "https://pypi.company.com/simple/"
```

---

### 9. `pip`에서 `uv`로 마이그레이션

#### 9.1 `requirements.txt`에서 마이그레이션

```bash
# 1. uv 프로젝트 초기화
uv init

# 2. requirements.txt 의존성을 pyproject.toml에 추가
uv add $(cat requirements.txt | grep -v '^#' | grep -v '^$' | tr '\n' ' ')

# 또는 개별적으로:
uv add fastapi uvicorn sqlalchemy  # requirements.txt의 패키지들

# 3. 동기화
uv sync
```

#### 9.2 `poetry`에서 마이그레이션

```bash
# 1. 이미 pyproject.toml이 있는 경우 (Poetry 형식)
# uv는 [project] 섹션의 PEP 621 형식을 사용합니다

# 2. Poetry의 [tool.poetry.dependencies]를 [project.dependencies]로 변환
# Before (Poetry):
# [tool.poetry.dependencies]
# python = "^3.12"
# fastapi = "^0.115.0"

# After (uv / PEP 621):
# [project]
# requires-python = ">=3.12"
# dependencies = ["fastapi>=0.115.0"]

# 3. uv lock 및 sync
uv lock
uv sync
```

#### 9.3 명령어 대응표

| 기존 도구 | uv 명령어 |
|-----------|-----------|
| `pip install package` | `uv add package` |
| `pip install -r requirements.txt` | `uv pip install -r requirements.txt` |
| `pip freeze > requirements.txt` | `uv pip freeze > requirements.txt` |
| `python -m venv .venv` | `uv venv` |
| `poetry add package` | `uv add package` |
| `poetry install` | `uv sync` |
| `poetry lock` | `uv lock` |
| `poetry run python main.py` | `uv run python main.py` |
| `pyenv install 3.12` | `uv python install 3.12` |
| `pipx run ruff` | `uvx ruff` |

---

### 10. 주요 설정 (`uv.toml` / `pyproject.toml`)

#### 프로젝트별 설정 (`pyproject.toml` 내 `[tool.uv]`)

```toml
[tool.uv]
# Python 버전 고정
python = "3.12"

# 개발 의존성 그룹
dev-dependencies = [
    "pytest>=8.0",
    "ruff>=0.8.0",
    "mypy>=1.13",
]
```

#### 전역 설정 (`~/.config/uv/uv.toml`)

```toml
# 글로벌 Python 버전
python = "3.12"

# 캐시 디렉토리 설정
cache-dir = "/path/to/cache"

# 기본 인덱스 URL
index-url = "https://pypi.org/simple/"
```

---

### 11. 실전 팁과 베스트 프랙티스

#### `.gitignore` 설정

```gitignore
# uv 가상 환경
.venv/

# Python 캐시
__pycache__/
*.pyc
```

> 💡 `uv.lock`은 반드시 Git에 커밋하세요! 팀 전체가 동일한 환경을 사용하려면 필수입니다.

#### CI/CD에서 uv 사용하기 (GitHub Actions 예시)

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v5
      
      - name: Set up Python
        run: uv python install
      
      - name: Install dependencies
        run: uv sync --all-groups
      
      - name: Run tests
        run: uv run pytest
      
      - name: Run linter
        run: uv run ruff check .
```

#### 자주 쓰는 명령어 모음

```bash
# 프로젝트 초기화
uv init my-project              # 앱 프로젝트
uv init --lib my-library        # 라이브러리 프로젝트

# 의존성 관리
uv add package                  # 의존성 추가
uv add package --dev            # 개발 의존성 추가
uv remove package               # 의존성 제거
uv sync                         # 의존성 동기화
uv lock                         # lock 파일만 업데이트
uv tree                         # 의존성 트리 보기

# 실행
uv run python main.py           # 스크립트 실행
uv run -m pytest                # 모듈 실행
uvx ruff check .                # 도구 일회성 실행

# Python 관리
uv python install 3.12          # Python 설치
uv python list                  # 설치된 Python 목록
uv python pin 3.12              # 버전 고정

# 패키지 빌드 및 배포
uv build                        # 패키지 빌드
uv publish                      # PyPI에 배포
```

---

## ❓ 자주 묻는 질문 (FAQ)

### Q1: `uv`는 `pip`를 완전히 대체할 수 있나요?

**A**: 네, 대부분의 경우 가능합니다. `uv`는 `pip`의 상위 호환이며, `uv pip install` 형태로 기존 `pip` 인터페이스도 제공합니다. 다만, 일부 레거시 패키지의 빌드 시스템(`setup.py` 기반)에서 호환 문제가 드물게 발생할 수 있습니다.

### Q2: `poetry`와 `uv`는 어떤 점이 다른가요?

**A**: 주요 차이점:

| 항목 | Poetry | uv |
|------|--------|-----|
| 언어 | Python | Rust |
| 속도 | 보통 | 매우 빠름 (10~100x) |
| 설정 형식 | `[tool.poetry]` (비표준) | `[project]` (PEP 621 표준) |
| Python 관리 | ❌ 별도 `pyenv` 필요 | ✅ 내장 |
| Lock 파일 | 단일 플랫폼 | 크로스 플랫폼 |
| pip 호환성 | ❌ | ✅ `uv pip` 인터페이스 |

### Q3: `uv.lock`과 `requirements.txt` 중 어떤 것을 써야 하나요?

**A**: **uv 프로젝트**에서는 `uv.lock`을 사용하세요. `requirements.txt`가 필요한 경우(Docker, 레거시 시스템 등):

```bash
# uv.lock으로부터 requirements.txt 생성
uv pip compile pyproject.toml -o requirements.txt

# 또는 uv export 사용
uv export --format requirements-txt > requirements.txt
```

### Q4: 가상 환경을 `.venv` 말고 다른 위치에 만들 수 있나요?

**A**: 네, 환경 변수로 설정 가능합니다:

```bash
# 환경 변수로 가상 환경 경로 지정
UV_PROJECT_ENVIRONMENT=/path/to/venv uv sync
```

### Q5: `uv run` 없이 직접 `python`을 써도 되나요?

**A**: 가상 환경을 직접 활성화(`source .venv/bin/activate`)한 후라면 가능합니다. 하지만 `uv run`을 사용하면:
- 가상 환경이 없으면 자동 생성
- 의존성이 최신이 아니면 자동 동기화
- 활성화/비활성화를 잊을 걱정이 없음

**`uv run` 사용을 권장합니다.**

### Q6: 특정 패키지만 업그레이드하고 싶어요

**A**:

```bash
# 특정 패키지 업그레이드
uv lock --upgrade-package fastapi
uv sync

# 모든 패키지를 최신 호환 버전으로 업그레이드
uv lock --upgrade
uv sync
```

### Q7: 기존 `requirements.txt` 프로젝트에서 바로 `uv`를 쓸 수 있나요?

**A**: 네! `uv`는 pip 호환 인터페이스도 제공합니다:

```bash
# pip 호환 모드로 설치 (마이그레이션 전)
uv pip install -r requirements.txt

# 정식 uv 프로젝트로 마이그레이션
uv init
uv add $(cat requirements.txt | grep -v '^#' | grep -v '^$' | tr '\n' ' ')
```

### Q8: 회사에서 프록시를 사용하는데, uv에서는 어떻게 설정하나요?

**A**: 표준 환경 변수를 지원합니다:

```bash
export HTTP_PROXY="http://proxy.company.com:8080"
export HTTPS_PROXY="http://proxy.company.com:8080"
export NO_PROXY="localhost,127.0.0.1"
```

### Q9: `uv`의 캐시는 어디에 저장되고, 얼마나 차지하나요?

**A**: 기본 캐시 위치:
- macOS: `~/Library/Caches/uv`
- Linux: `~/.cache/uv`
- Windows: `%LOCALAPPDATA%\uv\cache`

캐시 관리:
```bash
# 캐시 크기 확인
uv cache dir
du -sh $(uv cache dir)

# 캐시 정리
uv cache clean
```

### Q10: Docker에서 `uv`를 어떻게 사용하나요?

**A**: 공식 Docker 이미지를 활용합니다:

```dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .
CMD ["uv", "run", "python", "main.py"]
```

> 자세한 내용은 [05. Dockerfile](../05-dockerfile/README.md) 강의에서 다룹니다.

---

## 🏗️ 예제 프로젝트

| 예제 | 설명 | 핵심 학습 |
|------|------|----------|
| [01-basic-project](./examples/01-basic-project/) | 기본 uv 프로젝트 | `uv init`, `uv add`, `uv run` |
| [02-workspace](./examples/02-workspace/) | 모노레포 구성 | `workspace`, 패키지 간 참조 |

각 예제에는 실행 방법이 포함된 `README.md`가 있습니다.

---

## 🔗 참고 자료

- [uv 공식 문서](https://docs.astral.sh/uv/)
- [uv GitHub 저장소](https://github.com/astral-sh/uv)
- [PEP 621 - pyproject.toml 메타데이터 표준](https://peps.python.org/pep-0621/)
- [uv Docker 통합 가이드](https://docs.astral.sh/uv/guides/integration/docker/)
- [uv GitHub Actions 설정](https://docs.astral.sh/uv/guides/integration/github/)

---

## ⏭️ 다음 강의

[02. Python 패키징 기법 →](../02-python-packaging/README.md)
