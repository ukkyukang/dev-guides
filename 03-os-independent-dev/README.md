# 03. OS Independent 개발 방법론

> **"개발은 Windows(WSL)에서, 배포는 Docker(Linux)로"** — 2026년 클라우드 네이티브 개발 표준.  
> 하지만 Windows와 Linux는 근본이 다릅니다. 이 차이를 무시하면  
> **"내 윈도우 PC에서는 잘 되는데, 도커 컨테이너만 띄우면 죽어요!"** 라는 악몽이 시작됩니다.  
>  
> 이 강의에서는 OS에 종속되지 않는 무결점 코드를 작성하기 위한  
> **4가지 핵심 요소**와 **현대적 해결책(라이브러리)**을 다룹니다.


<!-- TOC -->
## 📑 목차

- [📋 사전 요구사항](#사전-요구사항)
- [🎯 학습 목표](#학습-목표)
- [📊 모던 파이썬 크로스 플랫폼 라이브러리 요약표](#모던-파이썬-크로스-플랫폼-라이브러리-요약표)
- [📖 본문](#본문)
  - [1. 파일 경로와 구분자 — `pathlib` (내장)](#1-파일-경로와-구분자-pathlib-내장)
    - [1.1 `os.path` → `pathlib` 변환 가이드](#11-ospath-pathlib-변환-가이드)
    - [1.2 파일 읽기/쓰기](#12-파일-읽기쓰기)
    - [1.3 디렉토리 생성 및 탐색](#13-디렉토리-생성-및-탐색)
  - [2. OS별 시스템 폴더 위치 — `platformdirs` (외부)](#2-os별-시스템-폴더-위치-platformdirs-외부)
    - [2.1 4가지 핵심 디렉토리](#21-4가지-핵심-디렉토리)
    - [2.2 실전 사용 패턴](#22-실전-사용-패턴)
  - [3. 환경 변수와 설정 관리 — `pydantic-settings` (외부)](#3-환경-변수와-설정-관리-pydantic-settings-외부)
    - [3.1 기본 사용법](#31-기본-사용법)
    - [3.2 우선순위](#32-우선순위)
    - [3.3 vs 기존 방식 비교](#33-vs-기존-방식-비교)
  - [4. 문자열 인코딩 — 한국어 Windows의 저주](#4-문자열-인코딩-한국어-windows의-저주)
    - [4.1 줄바꿈 문자](#41-줄바꿈-문자)
    - [4.2 `.gitattributes`로 줄바꿈 통일](#42-gitattributes로-줄바꿈-통일)
    - [4.3 macOS 한글 파일명 문제](#43-macos-한글-파일명-문제)
  - [5. 시스템 명령어 탐색 — `shutil.which()` (내장)](#5-시스템-명령어-탐색-shutilwhich-내장)
  - [6. 대소문자 민감도](#6-대소문자-민감도)
  - [7. 크로스 플랫폼 자동화](#7-크로스-플랫폼-자동화)
    - [7.1 `pyproject.toml` 스크립트](#71-pyprojecttoml-스크립트)
    - [7.2 Python 스크립트 (가장 확실한 방법)](#72-python-스크립트-가장-확실한-방법)
  - [8. 실전 체크리스트](#8-실전-체크리스트)
- [❓ 자주 묻는 질문 (FAQ)](#자주-묻는-질문-faq)
  - [Q1: `os.path`는 완전히 쓰지 말아야 하나요?](#q1-ospath는-완전히-쓰지-말아야-하나요)
  - [Q2: `platformdirs`의 config와 data 경로가 Windows에서 같은데요?](#q2-platformdirs의-config와-data-경로가-windows에서-같은데요)
  - [Q3: `pydantic-settings`에서 `.env` 파일이 없으면 에러가 나나요?](#q3-pydantic-settings에서-env-파일이-없으면-에러가-나나요)
  - [Q4: Docker에서 환경 변수와 `.env` 파일 중 뭐가 우선인가요?](#q4-docker에서-환경-변수와-env-파일-중-뭐가-우선인가요)
  - [Q5: `open()` 함수에서 `encoding` 파라미터를 항상 써야 하나요?](#q5-open-함수에서-encoding-파라미터를-항상-써야-하나요)
  - [Q6: CI/CD에서 여러 OS를 동시에 테스트하려면?](#q6-cicd에서-여러-os를-동시에-테스트하려면)
- [🏗️ 예제 프로젝트](#예제-프로젝트)
- [🔗 참고 자료](#참고-자료)
- [⏭️ 다음 강의](#다음-강의)

<!-- /TOC -->

---

## 📋 사전 요구사항

- [01. uv](../01-uv/README.md) 강의 완료
- Python 기본 문법 이해

## 🎯 학습 목표

이 강의를 완료하면 다음을 할 수 있습니다:

1. OS별 주요 차이점 4가지를 이해하고 대응 패턴을 적용할 수 있다
2. `pathlib`으로 크로스 플랫폼 경로를 처리할 수 있다
3. `platformdirs`로 OS별 표준 디렉토리를 자동 매핑할 수 있다
4. `pydantic-settings`로 환경 변수와 설정을 타입 안전하게 관리할 수 있다
5. 코드 한 글자 수정 없이 Windows에서도, Docker에서도 동작하는 앱을 만들 수 있다

---

## 📊 모던 파이썬 크로스 플랫폼 라이브러리 요약표

| 라이브러리 | 종류 | 기존 방식 (❌ 레거시) | 모던 방식 (✅ 2026 표준) | 도입 이유 |
|---|---|---|---|---|
| **`pathlib`** | 내장 | `os.path.join(a, b)` | `Path(a) / b` | 슬래시 하나로 OS 상관없이 경로 결합 |
| **`platformdirs`** | 외부 | `C:\\temp\\log` 하드코딩 | `user_log_dir("MyApp")` | OS별 표준 디렉토리 자동 매핑 |
| **`pydantic-settings`** | 외부 | `os.environ.get("PORT")` | `Settings()` 클래스 | `.env` 자동 로드 + 타입 검증 |
| **`shutil`** | 내장 | `os.system("dir")` | `shutil.which("git")` | 실행 파일 존재 여부 안전 확인 |

---

## 📖 본문

### 1. 파일 경로와 구분자 — `pathlib` (내장)

Windows와 Linux/macOS의 가장 근본적인 차이입니다.

| OS | 경로 구분자 | 예시 |
|----|-----------|------|
| Windows | `\` (백슬래시) | `C:\Users\dev\project` |
| macOS/Linux | `/` (슬래시) | `/home/dev/project` |

```python
# ❌ 레거시 — os.path (2026년 기준 구시대의 유물)
import os
path = os.path.join("src", "my_package", "config.json")

# ❌ 최악 — 하드코딩 (Windows에서만 동작)
path = "src\\my_package\\config.json"

# ✅ 모던 — pathlib.Path (2026 표준)
from pathlib import Path
path = Path("src") / "my_package" / "config.json"
# Windows: src\my_package\config.json
# Linux:   src/my_package/config.json
```

#### 1.1 `os.path` → `pathlib` 변환 가이드

| `os.path` (레거시) | `pathlib` (현대적) |
|--------------------|--------------------|
| `os.path.join("a", "b")` | `Path("a") / "b"` |
| `os.path.exists(path)` | `path.exists()` |
| `os.path.isfile(path)` | `path.is_file()` |
| `os.path.isdir(path)` | `path.is_dir()` |
| `os.path.basename(path)` | `path.name` |
| `os.path.dirname(path)` | `path.parent` |
| `os.path.splitext(path)` | `path.stem`, `path.suffix` |
| `os.path.abspath(path)` | `path.resolve()` |
| `os.path.expanduser("~")` | `Path.home()` |
| `os.getcwd()` | `Path.cwd()` |
| `os.listdir(path)` | `path.iterdir()` |
| `os.walk(path)` | `path.rglob("*")` |

#### 1.2 파일 읽기/쓰기

```python
from pathlib import Path

path = Path("data.txt")

# 쓰기
path.write_text("안녕하세요", encoding="utf-8")

# 읽기
text = path.read_text(encoding="utf-8")
```

#### 1.3 디렉토리 생성 및 탐색

```python
from pathlib import Path

# 디렉토리 생성 (부모까지 한 번에, 이미 있어도 에러 없음)
output_dir = Path("output") / "reports" / "2026"
output_dir.mkdir(parents=True, exist_ok=True)

# 재귀적 파일 탐색
for f in Path(".").rglob("*.py"):
    print(f)
```

---

### 2. OS별 시스템 폴더 위치 — `platformdirs` (외부)

앱이 로그/캐시/데이터를 저장해야 할 때, **절대로 경로를 하드코딩하지 마세요.**

```python
# ❌ 하드코딩 — 다른 OS에서 권한 오류(Permission Denied)로 뻗어버림
log_path = Path("C:\\temp\\my-app\\log")       # Windows에서만 동작
log_path = Path("/tmp/my-app/log")             # Linux에서만 동작
```

`platformdirs`에 **앱 이름만 알려주면**, 각 OS의 표준 규약에 맞는 안전한 폴더를 자동으로 찾아줍니다.

```bash
uv add platformdirs
```

#### 2.1 4가지 핵심 디렉토리

```python
from platformdirs import user_config_dir, user_data_dir, user_cache_dir, user_log_dir

app_name = "MyApp"

# 1. Config — 설정 파일 (settings.json 등)
config = user_config_dir(app_name)
# Windows:  C:\Users\user\AppData\Local\MyApp
# macOS:    ~/Library/Application Support/MyApp
# Linux:    ~/.config/MyApp

# 2. Data — 앱 데이터 (DB, 사용자 파일 등)
data = user_data_dir(app_name)
# Windows:  C:\Users\user\AppData\Local\MyApp
# macOS:    ~/Library/Application Support/MyApp
# Linux:    ~/.local/share/MyApp

# 3. Cache — 캐시 (지워져도 괜찮은 임시 데이터)
cache = user_cache_dir(app_name)
# Windows:  C:\Users\user\AppData\Local\MyApp\Cache
# macOS:    ~/Library/Caches/MyApp
# Linux:    ~/.cache/MyApp

# 4. Log — 로그 파일
log = user_log_dir(app_name)
# Windows:  C:\Users\user\AppData\Local\MyApp\Log
# macOS:    ~/Library/Logs/MyApp
# Linux:    ~/.local/state/MyApp/log
```

#### 2.2 실전 사용 패턴

```python
from pathlib import Path
from platformdirs import user_log_dir, user_data_dir

app_name = "MyApp"

# 로그 디렉토리 생성 + 로그 기록
log_dir = Path(user_log_dir(app_name))
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "app.log"

# UTF-8로 명시적 기록 (인코딩 방어)
with log_file.open("a", encoding="utf-8") as f:
    f.write("✅ 앱이 정상 시작되었습니다\n")

print(f"📂 로그 저장 위치: {log_file}")
# Windows 개발자: C:\Users\...\AppData\Local\MyApp\Log\app.log
# Docker(Linux):  ~/.local/state/MyApp/log/app.log
```

> 💡 **핵심**: 코드 한 글자 수정 없이, Windows에서도 Docker에서도 각 OS의 표준 경로에 자동 저장됩니다.

---

### 3. 환경 변수와 설정 관리 — `pydantic-settings` (외부)

기존 `os.environ.get()`의 문제점:
- 타입이 항상 `str` — `"8080"`을 `int`로 변환 잊으면 런타임 에러
- 필수 변수 누락을 컴파일 타임에 잡을 수 없음
- `.env` 파일과 시스템 환경 변수를 수동으로 합쳐야 함

```bash
uv add pydantic-settings
```

#### 3.1 기본 사용법

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """앱 설정 — .env 파일과 환경 변수를 자동으로 읽습니다."""

    app_name: str = "MyApp"
    debug: bool = False           # "true" → True 자동 변환
    port: int = 8080              # "8080" → 8080 자동 변환
    database_url: str = "sqlite:///data.db"
    secret_key: str              # 기본값 없음 → 필수 변수!

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",           # 정의하지 않은 변수는 무시
    )
```

```bash
# .env 파일 (Git에 커밋하지 마세요!)
APP_NAME=내프로젝트
DEBUG=true
PORT=3000
DATABASE_URL=postgresql://user:pass@localhost/mydb
SECRET_KEY=super-secret-key-12345
```

```python
# 사용
settings = AppSettings()

print(settings.app_name)      # "내프로젝트" (str)
print(settings.debug)          # True (bool — 자동 변환!)
print(settings.port)           # 3000 (int — 자동 변환!)
print(settings.database_url)   # "postgresql://..." (str)
```

#### 3.2 우선순위

`pydantic-settings`는 아래 순서로 설정을 읽습니다 (위가 우선):

1. **시스템 환경 변수** (Docker `ENV`, `export`)
2. **`.env` 파일**
3. **클래스의 기본값**

```bash
# Docker에서 환경 변수를 주입하면 .env보다 우선
docker run -e PORT=9090 my-app
# → settings.port = 9090 (환경 변수가 .env의 3000을 덮어씀)
```

#### 3.3 vs 기존 방식 비교

```python
# ❌ 레거시 — os.environ
import os
port = int(os.environ.get("PORT", "8080"))      # 수동 타입 변환
debug = os.environ.get("DEBUG") == "true"        # 수동 bool 변환
secret = os.environ.get("SECRET_KEY")            # None 체크 누락 위험
if secret is None:
    raise ValueError("SECRET_KEY 필수!")         # 런타임에야 발견

# ✅ 모던 — pydantic-settings
settings = AppSettings()                          # 모든 것이 자동!
# - 타입 변환 자동
# - 필수 변수 누락 시 즉시 ValidationError
# - .env 파일 자동 로드
```

---

### 4. 문자열 인코딩 — 한국어 Windows의 저주

한국어 Windows의 기본 텍스트 인코딩은 `CP949`(EUC-KR)입니다.

```python
# ❌ Windows에서 아무 생각 없이 쓰면...
with open("test.txt", "w") as f:
    f.write("안녕하세요")
# → CP949로 저장됨 → Docker(UTF-8)에서 읽으면 "뷃셣"

# ✅ 반드시 UTF-8을 명시!
with open("test.txt", "w", encoding="utf-8") as f:
    f.write("안녕하세요")

# ✅ pathlib으로 더 깔끔하게
from pathlib import Path
Path("test.txt").write_text("안녕하세요", encoding="utf-8")
```

#### 4.1 줄바꿈 문자

| OS | 줄바꿈 | 표현 |
|----|--------|------|
| Windows | CRLF | `\r\n` |
| macOS/Linux | LF | `\n` |

```python
# OS 독립적 줄 파싱
content = Path("data.txt").read_text(encoding="utf-8")
lines = content.splitlines()  # \n, \r\n, \r 모두 처리
```

#### 4.2 `.gitattributes`로 줄바꿈 통일

팀 전체에서 일관된 줄바꿈을 보장합니다:

```gitattributes
# 모든 텍스트 파일을 LF로 정규화
* text=auto eol=lf

# Windows 전용 스크립트만 CRLF 유지
*.bat text eol=crlf
*.cmd text eol=crlf
*.ps1 text eol=crlf

# 바이너리 파일
*.png binary
*.jpg binary
*.woff2 binary
```

#### 4.3 macOS 한글 파일명 문제

macOS의 APFS는 유니코드 NFD를 사용하여 한글을 분해 저장합니다:

```python
import unicodedata

# macOS에서 읽은 파일명을 NFC로 정규화
filename = unicodedata.normalize("NFC", raw_filename)
```

---

### 5. 시스템 명령어 탐색 — `shutil.which()` (내장)

```python
import shutil

# ❌ OS별 명령어 직접 실행
import os
os.system("ls")       # Linux에서만
os.system("dir")      # Windows에서만

# ✅ 명령어 존재 여부를 안전하게 확인
git = shutil.which("git")
docker = shutil.which("docker")

if git:
    print(f"✅ git 발견: {git}")
else:
    print("❌ git이 설치되어 있지 않습니다")

# subprocess도 리스트 형태로 (shell=True 사용 금지!)
import subprocess
subprocess.run(["python", "-m", "pytest"], check=True)
```

---

### 6. 대소문자 민감도

| OS | 파일 시스템 |
|----|-----------|
| Windows | 대소문자 무시 (`File.txt` == `file.txt`) |
| macOS (기본) | 대소문자 무시 (APFS 기본) |
| Linux / Docker | 대소문자 **구분** (`File.txt` ≠ `file.txt`) |

```python
# ❌ macOS/Windows에서는 되지만 Docker(Linux)에서 ImportError
from MyPackage import utils  # 실제 디렉토리는 mypackage

# ✅ 항상 정확한 대소문자 사용
from mypackage import utils
```

---

### 7. 크로스 플랫폼 자동화

#### 7.1 `pyproject.toml` 스크립트

```toml
[project.scripts]
dev = "my_app.cli:dev_server"
```

```bash
# 어떤 OS에서든 동일
uv run dev
uv run -m pytest
```

#### 7.2 Python 스크립트 (가장 확실한 방법)

Makefile은 Windows에서 `make`를 설치해야 합니다. Python 스크립트가 가장 확실합니다:

```python
#!/usr/bin/env python3
"""dev.py — 크로스 플랫폼 개발 자동화."""
import subprocess, sys

def run(cmd):
    print(f"▶ {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

commands = {
    "test":   lambda: run([sys.executable, "-m", "pytest", "-v"]),
    "lint":   lambda: run([sys.executable, "-m", "ruff", "check", "src/"]),
    "format": lambda: run([sys.executable, "-m", "ruff", "format", "src/"]),
}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    if cmd not in commands:
        print(f"사용법: python dev.py [{' | '.join(commands)}]")
        sys.exit(1)
    commands[cmd]()
```

---

### 8. 실전 체크리스트

프로젝트가 크로스 플랫폼에서 올바르게 동작하는지 확인하세요:

- [ ] 모든 경로가 `pathlib.Path`를 사용하는가?
- [ ] 파일 읽기/쓰기에 `encoding="utf-8"`을 명시했는가?
- [ ] 로그/캐시/데이터 경로에 `platformdirs`를 사용하는가?
- [ ] 환경 변수를 `pydantic-settings`로 관리하는가?
- [ ] `.gitattributes`에서 줄바꿈 정규화가 설정되어 있는가?
- [ ] 하드코딩된 OS 전용 경로(`C:\...`, `/home/...`)가 없는가?
- [ ] `subprocess` 호출이 리스트 형태인가 (`shell=True` 미사용)?
- [ ] import 경로의 대소문자가 실제 디렉토리와 일치하는가?

---

## ❓ 자주 묻는 질문 (FAQ)

### Q1: `os.path`는 완전히 쓰지 말아야 하나요?

**A**: **새 코드에서는 `pathlib`만 사용하세요.** `os.path`는 레거시입니다. 모든 표준 라이브러리와 프레임워크가 `pathlib.Path`를 지원합니다. 문자열이 필요한 경우 `str(path)`로 변환 가능합니다.

### Q2: `platformdirs`의 config와 data 경로가 Windows에서 같은데요?

**A**: 맞습니다. Windows는 `AppData\Local`에 통합 저장하는 것이 관례입니다. Linux에서는 `~/.config` (config)와 `~/.local/share` (data)로 분리됩니다. `platformdirs`가 각 OS의 관례를 자동으로 따릅니다.

### Q3: `pydantic-settings`에서 `.env` 파일이 없으면 에러가 나나요?

**A**: 아닙니다. `env_file=".env"`로 설정해도 파일이 없으면 조용히 무시합니다. 시스템 환경 변수나 기본값만 사용됩니다.

### Q4: Docker에서 환경 변수와 `.env` 파일 중 뭐가 우선인가요?

**A**: **시스템 환경 변수(`docker run -e`)가 `.env` 파일보다 우선**합니다. 이는 Docker 운영 시 `.env` 기본값을 환경 변수로 덮어쓸 수 있어 매우 유용합니다.

### Q5: `open()` 함수에서 `encoding` 파라미터를 항상 써야 하나요?

**A**: **네.** Python 3.14 이전까지 Windows에서 `open()`의 기본 인코딩이 시스템 로캘(한국어: CP949)을 따릅니다. Docker는 UTF-8이므로 반드시 명시하세요.

### Q6: CI/CD에서 여러 OS를 동시에 테스트하려면?

**A**: GitHub Actions의 `matrix`:
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
runs-on: ${{ matrix.os }}
```

---

## 🏗️ 예제 프로젝트

| 예제 | 설명 | 핵심 학습 |
|------|------|----------|
| [01-path-handling](./examples/01-path-handling/) | pathlib 기반 경로 처리 | Path, 인코딩, 파일 I/O |
| [02-cross-platform-script](./examples/02-cross-platform-script/) | 자동화 스크립트 | subprocess, Taskfile |
| [03-cross-platform-demo](./examples/03-cross-platform-demo/) | **Streamlit 데모 앱 ⭐** | pathlib + platformdirs + pydantic-settings 통합 |

---

## 🔗 참고 자료

- [pathlib 공식 문서](https://docs.python.org/3/library/pathlib.html)
- [platformdirs 라이브러리](https://pypi.org/project/platformdirs/)
- [pydantic-settings 공식 문서](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [PEP 686 — UTF-8 기본 인코딩](https://peps.python.org/pep-0686/)

---

## ⏭️ 다음 강의

[04. WSL과 Docker & Docker Registry →](../04-wsl-docker-registry/README.md)
