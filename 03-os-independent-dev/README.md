# 03. OS Independent 개발 방법론

> Windows, macOS, Linux 어디서나 동일하게 동작하는 코드를 작성하는 방법을 배웁니다.  
> 경로 처리, 줄바꿈, 인코딩, 환경 변수 등 실무에서 자주 마주치는 함정을 다룹니다.

---

## 📋 사전 요구사항

- [01. uv](../01-uv/README.md) 강의 완료
- Python 기본 문법 이해
- 여러 OS에서 개발한 경험이 있으면 좋음 (필수 아님)

## 🎯 학습 목표

이 강의를 완료하면 다음을 할 수 있습니다:

1. OS별 주요 차이점을 이해하고 대응 패턴을 적용할 수 있다
2. `pathlib`을 활용하여 크로스 플랫폼 경로를 처리할 수 있다
3. 파일 인코딩 문제를 예방하고 해결할 수 있다
4. 환경 변수와 설정 파일을 OS 독립적으로 관리할 수 있다
5. 크로스 플랫폼 자동화 스크립트를 작성할 수 있다

---

## 📖 본문

### 1. OS별 주요 차이점

개발을 하다 보면 "내 컴퓨터에서는 되는데..."라는 말을 자주 듣게 됩니다. 대부분 아래 차이점 때문입니다.

#### 1.1 경로 구분자

| OS | 경로 구분자 | 예시 |
|----|-----------|------|
| Windows | `\` (백슬래시) | `C:\Users\dev\project` |
| macOS/Linux | `/` (슬래시) | `/home/dev/project` |

```python
# ❌ 하드코딩된 경로 — Windows에서만 동작
path = "src\\my_package\\config.json"

# ❌ 하드코딩된 경로 — Unix에서만 동작
path = "src/my_package/config.json"

# ✅ OS 독립적 — 어디서나 동작
from pathlib import Path
path = Path("src") / "my_package" / "config.json"
```

#### 1.2 줄바꿈 문자

| OS | 줄바꿈 | 표현 |
|----|--------|------|
| Windows | CRLF | `\r\n` |
| macOS/Linux | LF | `\n` |

```python
# ❌ 문제 발생 가능
with open("data.txt", "r") as f:
    content = f.read()
    # Windows에서 \r\n이 남아있을 수 있음

# ✅ newline 파라미터로 제어
with open("data.txt", "r", newline="") as f:
    content = f.read()
    # 줄바꿈을 있는 그대로 읽음

# ✅ 또는 splitlines()으로 OS 독립적 파싱
lines = content.splitlines()  # \n, \r\n, \r 모두 처리
```

> 💡 **`.gitattributes`로 해결하기**: Git에서 자동 변환을 설정하세요:
> ```
> # .gitattributes
> * text=auto eol=lf
> *.bat text eol=crlf
> *.ps1 text eol=crlf
> ```

#### 1.3 파일 인코딩

| OS | 기본 인코딩 |
|----|-----------|
| Windows (한국어) | `cp949` (EUC-KR) |
| macOS/Linux | `UTF-8` |

```python
# ❌ Windows에서 한글 파일을 읽을 때 깨질 수 있음
with open("data.txt") as f:
    content = f.read()  # 시스템 기본 인코딩 사용

# ✅ 항상 인코딩을 명시
with open("data.txt", encoding="utf-8") as f:
    content = f.read()
```

> 💡 **Python 3.15+**: UTF-8이 기본 인코딩이 될 예정입니다 (PEP 686).
> 그 전까지는 반드시 `encoding="utf-8"`을 명시하세요.

#### 1.4 대소문자 민감도

| OS | 파일 시스템 대소문자 |
|----|-------------------|
| Windows | 대소문자 무시 (`File.txt` == `file.txt`) |
| macOS (기본) | 대소문자 무시 (APFS 기본 설정) |
| Linux | 대소문자 구분 (`File.txt` ≠ `file.txt`) |

```python
# ❌ macOS/Windows에서는 동작하지만 Linux CI/CD에서 실패
from MyPackage import utils  # 실제 디렉토리는 mypackage

# ✅ 항상 정확한 대소문자 사용
from mypackage import utils
```

#### 1.5 환경 변수

```python
import os

# 경로 리스트 구분자
# Windows: PATH = "C:\Python;C:\Tools"     (세미콜론)
# Unix:    PATH = "/usr/bin:/usr/local/bin" (콜론)
path_sep = os.pathsep  # Windows: ";", Unix: ":"

# 홈 디렉토리
home = Path.home()  # 모든 OS에서 작동

# 임시 디렉토리
import tempfile
tmp = Path(tempfile.gettempdir())  # 모든 OS에서 작동
```

---

### 2. `pathlib` — 경로 처리의 정석

`pathlib`은 Python 3.4에서 도입된 객체 지향 파일 시스템 경로 라이브러리입니다.
**2026년 기준, 모든 새 코드에서 `os.path` 대신 `pathlib`을 사용해야 합니다.**

#### 2.1 기본 사용법

```python
from pathlib import Path

# 경로 생성
project_root = Path(__file__).parent.parent   # 현재 파일 기준 상대 경로
config_path = project_root / "config" / "settings.json"  # / 연산자로 결합

# 경로 정보
print(config_path.name)        # "settings.json"
print(config_path.stem)        # "settings"
print(config_path.suffix)      # ".json"
print(config_path.parent)      # .../config
print(config_path.parts)       # ('...', 'config', 'settings.json')
print(config_path.is_absolute())  # True/False
```

#### 2.2 `os.path` → `pathlib` 변환 가이드

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

#### 2.3 파일 읽기/쓰기

```python
from pathlib import Path

path = Path("data.txt")

# 쓰기
path.write_text("안녕하세요", encoding="utf-8")
path.write_bytes(b"\x89PNG...")

# 읽기
text = path.read_text(encoding="utf-8")
data = path.read_bytes()
```

#### 2.4 디렉토리 탐색

```python
from pathlib import Path

project = Path(".")

# 현재 디렉토리의 파일만
for f in project.iterdir():
    print(f.name)

# 특정 패턴의 파일 (현재 디렉토리만)
for f in project.glob("*.py"):
    print(f)

# 재귀적으로 모든 하위 디렉토리 포함
for f in project.rglob("*.py"):
    print(f)

# 특정 패턴 매칭
for f in project.rglob("test_*.py"):
    print(f)
```

#### 2.5 디렉토리/파일 생성

```python
from pathlib import Path

# 디렉토리 생성 (부모 디렉토리도 함께, 이미 존재해도 에러 없음)
output_dir = Path("output") / "reports" / "2026"
output_dir.mkdir(parents=True, exist_ok=True)

# 파일 생성
(output_dir / "report.txt").write_text("보고서 내용", encoding="utf-8")
```

---

### 3. 환경 변수와 설정 관리

#### 3.1 환경 변수 읽기

```python
import os

# 기본값 포함 읽기
db_host = os.environ.get("DB_HOST", "localhost")
db_port = int(os.environ.get("DB_PORT", "5432"))
debug = os.environ.get("DEBUG", "false").lower() == "true"
```

#### 3.2 `.env` 파일 활용

```bash
# .env 파일 (Git에 커밋하지 마세요!)
DB_HOST=localhost
DB_PORT=5432
DEBUG=true
SECRET_KEY=your-secret-key
```

```python
# python-dotenv 사용
# uv add python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()  # .env 파일을 환경 변수로 로드

db_host = os.environ.get("DB_HOST", "localhost")
```

#### 3.3 OS별 설정 파일 위치

```python
from pathlib import Path
import platform

def get_config_dir(app_name: str) -> Path:
    """OS에 맞는 설정 파일 디렉토리를 반환합니다."""
    system = platform.system()
    
    if system == "Windows":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    elif system == "Darwin":  # macOS
        base = Path.home() / "Library" / "Application Support"
    else:  # Linux
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    
    config_dir = base / app_name
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir

# 사용
config = get_config_dir("my-app")
# Windows: C:\Users\user\AppData\Roaming\my-app
# macOS:   /Users/user/Library/Application Support/my-app
# Linux:   /home/user/.config/my-app
```

> 💡 **팁**: [`platformdirs`](https://pypi.org/project/platformdirs/) 라이브러리를 사용하면 위 코드를 직접 작성할 필요가 없습니다:
> ```python
> from platformdirs import user_config_dir
> config_path = Path(user_config_dir("my-app"))
> ```

---

### 4. 프로세스 실행

#### 4.1 `subprocess` 크로스 플랫폼 사용

```python
import subprocess
import shutil

# ❌ 셸 명령어 직접 사용 — OS마다 다름
subprocess.run("ls -la", shell=True)          # Linux/macOS만
subprocess.run("dir", shell=True)             # Windows만

# ✅ 리스트 형태로 실행 — 셸 의존 없음
subprocess.run(["python", "-m", "pytest"], check=True)

# ✅ 실행 파일 존재 확인
if shutil.which("git"):
    subprocess.run(["git", "status"], check=True)
else:
    print("git이 설치되어 있지 않습니다")
```

#### 4.2 셸 스크립트 대안

```python
import sys
import platform

def get_python_executable() -> str:
    """현재 Python 실행 파일 경로를 반환합니다."""
    return sys.executable

def is_windows() -> bool:
    """Windows OS인지 확인합니다."""
    return platform.system() == "Windows"

def is_macos() -> bool:
    """macOS인지 확인합니다."""
    return platform.system() == "Darwin"

def is_linux() -> bool:
    """Linux인지 확인합니다."""
    return platform.system() == "Linux"
```

---

### 5. 크로스 플랫폼 자동화

#### 5.1 `pyproject.toml` 스크립트 (uv 활용)

개발 작업을 `pyproject.toml`의 스크립트로 정의하면 어떤 OS에서든 동일하게 실행됩니다:

```toml
[project.scripts]
dev = "my_app.cli:dev_server"
```

```bash
# 어떤 OS에서든 동일
uv run dev
uv run -m pytest
uv run -m mypy src/
```

#### 5.2 Makefile vs Taskfile

**Makefile** (Linux/macOS에서 주로 사용):

```makefile
.PHONY: test lint format

test:
	uv run pytest

lint:
	uv run ruff check src/

format:
	uv run ruff format src/
```

> ⚠️ Makefile은 Windows에서 `make`를 별도 설치해야 합니다.

**[Taskfile](https://taskfile.dev/)** (크로스 플랫폼 권장 ✅):

```yaml
# Taskfile.yml
version: '3'

tasks:
  test:
    desc: "테스트 실행"
    cmds:
      - uv run pytest

  lint:
    desc: "린트 검사"
    cmds:
      - uv run ruff check src/

  format:
    desc: "코드 포맷팅"
    cmds:
      - uv run ruff format src/

  all:
    desc: "전체 검사"
    deps: [lint, test]
```

```bash
# 어떤 OS에서든 동일
task test
task lint
task all
```

#### 5.3 Python 스크립트로 자동화 (가장 확실한 방법)

```python
#!/usr/bin/env python3
"""dev.py — 크로스 플랫폼 개발 스크립트."""

import subprocess
import sys


def run(cmd: list[str]) -> None:
    """명령어를 실행하고 실패 시 종료합니다."""
    print(f"▶ {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)


def test():
    run([sys.executable, "-m", "pytest", "-v"])


def lint():
    run([sys.executable, "-m", "ruff", "check", "src/"])


def format_code():
    run([sys.executable, "-m", "ruff", "format", "src/"])


if __name__ == "__main__":
    commands = {
        "test": test,
        "lint": lint,
        "format": format_code,
    }

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print(f"사용법: python dev.py [{' | '.join(commands)}]")
        sys.exit(1)

    commands[sys.argv[1]]()
```

---

### 6. `.gitattributes` 설정

팀 전체에서 일관된 줄바꿈과 인코딩을 보장합니다:

```gitattributes
# 모든 텍스트 파일의 줄바꿈을 LF로 정규화
* text=auto eol=lf

# Windows 전용 파일은 CRLF 유지
*.bat text eol=crlf
*.cmd text eol=crlf
*.ps1 text eol=crlf

# 바이너리 파일 자동 감지
*.png binary
*.jpg binary
*.ico binary
*.woff2 binary
```

---

### 7. 실전 체크리스트

프로젝트가 크로스 플랫폼에서 올바르게 동작하는지 확인하세요:

- [ ] 모든 경로가 `pathlib.Path`를 사용하고 있는가?
- [ ] 파일 읽기/쓰기에 `encoding="utf-8"`을 명시했는가?
- [ ] `.gitattributes`에서 줄바꿈 정규화를 설정했는가?
- [ ] 하드코딩된 OS 전용 경로(`C:\...`, `/home/...`)가 없는가?
- [ ] `subprocess` 호출이 리스트 형태인가 (`shell=True` 미사용)?
- [ ] import 경로의 대소문자가 실제 디렉토리와 일치하는가?
- [ ] 임시 파일/디렉토리에 `tempfile` 모듈을 사용하는가?

---

## ❓ 자주 묻는 질문 (FAQ)

### Q1: `os.path`와 `pathlib` 중 어떤 것을 써야 하나요?

**A**: **`pathlib`을 사용하세요.** `os.path`는 레거시 코드에서만 유지합니다. 모든 표준 라이브러리와 주요 프레임워크가 `pathlib.Path`를 지원합니다. `Path` 객체는 `str(path)`로 언제든 문자열로 변환 가능합니다.

### Q2: Windows에서 경로가 260자 제한에 걸립니다

**A**: Windows 10 이상에서는 레지스트리 설정으로 긴 경로를 활성화할 수 있습니다:
```
HKLM\SYSTEM\CurrentControlSet\Control\FileSystem\LongPathsEnabled = 1
```
또는 Python에서: `Path("\\\\?\\C:\\very\\long\\path\\...")`

### Q3: `open()` 함수에서 `encoding` 파라미터를 항상 써야 하나요?

**A**: **네.** Python 3.14 이전까지는 Windows에서 `open()`의 기본 인코딩이 `cp949`(한국어) 또는 시스템 로캘을 따릅니다. UTF-8이 아닌 인코딩에서 한글 파일이 깨질 수 있습니다.

```python
# 반드시 이렇게!
with open("file.txt", encoding="utf-8") as f:
    ...
```

### Q4: macOS에서 파일 이름의 한글이 깨지는 문제가 있습니다

**A**: macOS의 APFS/HFS+는 유니코드 NFD(Normalization Form Decomposition)를 사용합니다. `ㅎ + ㅏ + ㄴ`처럼 글자를 분해하여 저장합니다.

```python
import unicodedata

# macOS에서 읽은 파일명을 NFC로 정규화
filename = unicodedata.normalize("NFC", raw_filename)
```

### Q5: CI/CD에서 Linux를 쓰는데, 로컬은 Windows/macOS입니다. 어떻게 테스트하나요?

**A**: 여러 전략이 있습니다:
1. **Docker**: 로컬에서 Linux 컨테이너로 테스트 (강의 05~07 참고)
2. **GitHub Actions의 `matrix`**: 여러 OS에서 동시 테스트
   ```yaml
   strategy:
     matrix:
       os: [ubuntu-latest, windows-latest, macos-latest]
   ```
3. **WSL**: Windows에서 Linux 환경 사용

### Q6: `shutil.which()`가 무엇인가요?

**A**: 시스템 PATH에서 실행 파일을 찾는 크로스 플랫폼 함수입니다. Windows에서는 `.exe`, `.bat` 등의 확장자도 자동 검색합니다.

```python
import shutil

git = shutil.which("git")       # "/usr/bin/git" 또는 "C:\Program Files\Git\cmd\git.exe"
node = shutil.which("node")     # None (미설치 시)
```

---

## 🏗️ 예제 프로젝트

| 예제 | 설명 | 핵심 학습 |
|------|------|----------|
| [01-path-handling](./examples/01-path-handling/) | pathlib 기반 크로스 플랫폼 경로 처리 | Path, 인코딩, 파일 I/O |
| [02-cross-platform-script](./examples/02-cross-platform-script/) | 크로스 플랫폼 자동화 스크립트 | subprocess, Taskfile |

---

## 🔗 참고 자료

- [pathlib 공식 문서](https://docs.python.org/3/library/pathlib.html)
- [PEP 428 — pathlib 도입](https://peps.python.org/pep-0428/)
- [PEP 686 — UTF-8 기본 인코딩](https://peps.python.org/pep-0686/)
- [Taskfile 공식 문서](https://taskfile.dev/)
- [platformdirs 라이브러리](https://pypi.org/project/platformdirs/)

---

## ⏭️ 다음 강의

[04. WSL과 Docker & Docker Registry →](../04-wsl-docker-registry/README.md)
