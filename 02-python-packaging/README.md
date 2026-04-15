# 02. Python 패키징 기법

> Python 프로젝트를 재사용 가능한 패키지로 만드는 현대적인 방법을 배웁니다.  
> `pyproject.toml` 표준, src layout, 네임스페이스 패키지, 사설 인덱스 배포까지 다룹니다.

---

## 📋 사전 요구사항

- [01. uv](../01-uv/README.md) 강의 완료
- `pyproject.toml` 기본 구조 이해
- Python 모듈과 패키지 (`import`) 기초

## 🎯 학습 목표

이 강의를 완료하면 다음을 할 수 있습니다:

1. `pyproject.toml` 기반의 현대적 패키지 구조를 설계할 수 있다
2. `src` layout과 `flat` layout의 차이를 이해하고 선택할 수 있다
3. 빌드 시스템(`hatchling`, `setuptools` 등)의 역할을 이해한다
4. 네임스페이스 패키지를 구성하여 조직 단위로 패키지를 관리할 수 있다
5. 사설 PyPI 인덱스에 패키지를 배포할 수 있다

---

## 📖 본문

### 1. Python 패키지란?

Python에서 **패키지**는 관련 모듈을 하나의 디렉토리 구조로 묶은 것입니다.

```
my_package/
├── __init__.py        # 이 디렉토리가 패키지임을 나타냄
├── module_a.py
└── sub_package/
    ├── __init__.py
    └── module_b.py
```

```python
# 사용 예시
from my_package import module_a
from my_package.sub_package import module_b
```

**배포 가능한 패키지**는 여기에 메타데이터(`pyproject.toml`)를 추가하여 다른 사람이 `pip install`로 설치할 수 있도록 만든 것입니다.

---

### 2. 현대적 패키지 구조: `pyproject.toml`

Python 패키징은 오랫동안 `setup.py`, `setup.cfg`, `requirements.txt` 등 여러 파일의 조합으로 이루어졌습니다. **2026년 현재, `pyproject.toml` 하나로 모든 것을 관리**하는 것이 표준입니다.

#### 2.1 핵심 표준 (PEP)

| PEP | 제목 | 설명 |
|-----|------|------|
| [PEP 517](https://peps.python.org/pep-0517/) | Build system interface | 빌드 백엔드 인터페이스 표준 |
| [PEP 518](https://peps.python.org/pep-0518/) | Build system requirements | `[build-system]` 테이블 도입 |
| [PEP 621](https://peps.python.org/pep-0621/) | Project metadata | `[project]` 테이블로 메타데이터 표준화 |
| [PEP 660](https://peps.python.org/pep-0660/) | Editable installs | 개발 모드 설치 표준화 |

#### 2.2 `pyproject.toml` 전체 구조

```toml
# ============================================================
# 프로젝트 메타데이터 (PEP 621)
# ============================================================
[project]
name = "my-package"                      # PyPI에서의 패키지 이름
version = "1.0.0"                         # 시맨틱 버전
description = "패키지에 대한 간결한 설명"
readme = "README.md"                      # 상세 설명 파일
license = { text = "MIT" }
requires-python = ">=3.11"
authors = [
    { name = "홍길동", email = "gildong@example.com" },
]
keywords = ["example", "packaging"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.12",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

# 런타임 의존성
dependencies = [
    "httpx>=0.27.0",
    "pydantic>=2.0",
]

# 선택적 의존성 (extras)
[project.optional-dependencies]
dev = ["pytest>=8.0", "ruff>=0.8.0", "mypy>=1.13"]
docs = ["mkdocs>=1.6", "mkdocs-material>=9.5"]

# CLI 엔트리포인트
[project.scripts]
my-cli = "my_package.cli:main"

# URL 링크
[project.urls]
Homepage = "https://github.com/example/my-package"
Documentation = "https://my-package.readthedocs.io"
Repository = "https://github.com/example/my-package"
Issues = "https://github.com/example/my-package/issues"

# ============================================================
# 빌드 시스템
# ============================================================
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# ============================================================
# 도구별 설정
# ============================================================
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.mypy]
python_version = "3.12"
strict = true
```

#### 2.3 각 섹션 상세 설명

**`name`**: PyPI에서의 고유 이름. 하이픈(`-`) 또는 언더스코어(`_`)를 사용합니다. PyPI에서는 둘을 동일하게 취급합니다.

```
pyproject.toml의 name    →    import할 때 이름
"my-package"             →    my_package
"company-utils"          →    company.utils (네임스페이스 패키지의 경우)
```

**`version`**: [시맨틱 버전](https://semver.org/lang/ko/)을 따릅니다.

```
MAJOR.MINOR.PATCH
  │     │     └── 버그 수정 (하위 호환)
  │     └──────── 기능 추가 (하위 호환)
  └────────────── 호환성 깨지는 변경
```

**`requires-python`**: 지원하는 Python 버전 범위.

```toml
requires-python = ">=3.11"       # 3.11 이상
requires-python = ">=3.11,<4"    # 3.11 이상, 4.0 미만
```

**`dependencies`**: 버전 지정 방식:

```toml
dependencies = [
    "httpx",                  # 아무 버전 (비권장)
    "httpx>=0.27.0",          # 0.27.0 이상
    "httpx>=0.27.0,<1.0",     # 0.27.0 이상, 1.0 미만
    "httpx~=0.27.0",          # 0.27.0 이상, 0.28.0 미만 (호환 릴리스)
    "httpx==0.27.2",          # 정확한 버전 (비권장, lock 파일이 이 역할)
]
```

**`[project.scripts]`**: 설치 시 생성되는 CLI 명령어:

```toml
[project.scripts]
my-cli = "my_package.cli:main"     # my_package/cli.py의 main() 함수 실행
```

설치 후:
```bash
$ my-cli --help    # 터미널에서 바로 실행 가능
```

---

### 3. 프로젝트 레이아웃

#### 3.1 Src Layout (권장 ✅)

```
my-project/
├── pyproject.toml
├── README.md
├── src/
│   └── my_package/
│       ├── __init__.py
│       └── core.py
└── tests/
    └── test_core.py
```

**장점**:
- 소스 코드가 `src/` 아래에 격리되어 있어, 실수로 설치되지 않은 패키지를 import하는 것을 방지
- 테스트가 항상 **설치된 버전**의 패키지를 테스트 (editable install 포함)
- 패키지 코드와 프로젝트 설정 파일이 깔끔하게 분리

**빌드 설정**:
```toml
[tool.hatch.build.targets.wheel]
packages = ["src/my_package"]
```

#### 3.2 Flat Layout

```
my-project/
├── pyproject.toml
├── README.md
├── my_package/
│   ├── __init__.py
│   └── core.py
└── tests/
    └── test_core.py
```

**장점**:
- 단순한 구조, 소규모 프로젝트에 적합
- 빌드 설정이 간단 (빌드 백엔드가 자동 감지)

**단점**:
- 프로젝트 루트에서 `import my_package`가 설치 전에도 동작하여, 테스트 시 **미설치 상태**를 감지 못할 수 있음

#### 3.3 어떤 레이아웃을 선택해야 하나?

| 상황 | 권장 레이아웃 |
|------|-------------|
| 라이브러리 패키지 (배포 목적) | **Src Layout** ✅ |
| 사내 공유 패키지 | **Src Layout** ✅ |
| 간단한 스크립트 / 앱 | Flat Layout |
| 모노레포 내 패키지 | **Src Layout** ✅ |

> 💡 **결론**: 특별한 이유가 없다면 **Src Layout**을 사용하세요.

---

### 4. 빌드 시스템 이해

빌드 시스템은 소스 코드를 설치 가능한 패키지(wheel, sdist)로 변환합니다.

#### 4.1 주요 빌드 백엔드 비교

| 빌드 백엔드 | 특징 | 추천 상황 |
|------------|------|----------|
| **hatchling** | 빠르고 현대적, PEP 621 네이티브 | 🏆 **대부분의 프로젝트** (권장) |
| **setuptools** | 가장 오래된 표준, 레거시 지원 | 기존 setuptools 프로젝트 유지 |
| **flit-core** | 매우 가볍고 간단 | 순수 Python 라이브러리 |
| **maturin** | Rust 확장 모듈 빌드 | PyO3 기반 프로젝트 |
| **pdm-backend** | PDM 기반 | PDM 사용 프로젝트 |

#### 4.2 빌드 결과물

```bash
# 패키지 빌드
uv build

# 결과물 (dist/ 디렉토리에 생성)
dist/
├── my_package-1.0.0.tar.gz          # sdist (소스 배포)
└── my_package-1.0.0-py3-none-any.whl  # wheel (바이너리 배포)
```

**sdist (Source Distribution)**: 소스 코드 압축 파일. 설치 시 빌드 과정 필요.  
**wheel**: 사전 빌드된 패키지. 설치가 빠르고 빌드 도구 불필요.

#### 4.3 `[build-system]` 설정 예시

```toml
# hatchling (권장)
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# setuptools (레거시)
[build-system]
requires = ["setuptools>=75.0", "wheel"]
build-backend = "setuptools.build_meta"

# flit
[build-system]
requires = ["flit_core>=3.4"]
build-backend = "flit_core.buildapi"
```

---

### 5. 네임스페이스 패키지

네임스페이스 패키지는 **하나의 최상위 패키지 이름 아래에 여러 독립 패키지를 그룹화**하는 기법입니다.

#### 5.1 왜 필요한가?

대형 조직에서는 여러 팀이 각각의 라이브러리를 개발합니다:

```
company.core        ← 플랫폼 팀이 개발
company.auth        ← 인증 팀이 개발
company.ml          ← ML 팀이 개발
```

각 패키지는 **독립적으로 설치 가능**하지만, 사용할 때는:

```python
from company.core import BaseModel
from company.auth import authenticate
from company.ml import predict
```

모두 `company` 네임스페이스 아래에서 일관된 import 경로를 제공합니다.

#### 5.2 구현 방법 (Implicit Namespace Package)

**핵심 규칙**: `company/` 디렉토리에 `__init__.py`를 **넣지 않습니다**.

```
packages/
├── company-core/
│   ├── pyproject.toml
│   └── src/
│       └── company/               # ❌ __init__.py 없음!
│           └── core/
│               ├── __init__.py    # ✅ 여기부터 __init__.py
│               └── models.py
├── company-auth/
│   ├── pyproject.toml
│   └── src/
│       └── company/               # ❌ __init__.py 없음!
│           └── auth/
│               ├── __init__.py    # ✅
│               └── handlers.py
```

각 패키지의 `pyproject.toml`:

```toml
# company-core/pyproject.toml
[project]
name = "company-core"
version = "1.0.0"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/company"]
```

> ⚠️ **주의**: `company/__init__.py`를 만들면 네임스페이스가 깨집니다! Python의 implicit namespace package 메커니즘은 `__init__.py`가 없을 때만 작동합니다.

#### 5.3 사내 네임스페이스 패키지 관례

```
# 추천 네이밍 컨벤션
{회사이름}-{기능}

# PyPI/사설 인덱스의 패키지 이름
company-core
company-auth
company-ml

# Python import 경로
from company.core import ...
from company.auth import ...
from company.ml import ...
```

---

### 6. 패키지 배포

#### 6.1 PyPI에 배포

```bash
# 1. 빌드
uv build

# 2. PyPI에 배포 (API 토큰 필요)
uv publish --token pypi-xxxxx

# 또는 환경 변수 사용
export UV_PUBLISH_TOKEN=pypi-xxxxx
uv publish
```

#### 6.2 사설 인덱스에 배포

회사 내부의 사설 PyPI 서버(예: DevPI, Artifactory, Nexus)에 배포:

```bash
# 사설 인덱스에 배포
uv publish \
  --publish-url https://pypi.company.com/upload/ \
  --username deploy \
  --password $PYPI_TOKEN
```

#### 6.3 사설 인덱스에서 설치

```toml
# pyproject.toml
[tool.uv]
index-url = "https://pypi.org/simple/"    # 기본 인덱스

[[tool.uv.index]]
name = "company"
url = "https://pypi.company.com/simple/"

# 특정 패키지를 사설 인덱스에서 가져오기
[tool.uv.sources]
company-core = { index = "company" }
company-auth = { index = "company" }
```

#### 6.4 버전 관리 전략

##### 수동 버전 관리

`pyproject.toml`에서 직접 버전을 변경:

```toml
[project]
version = "1.2.3"
```

##### 동적 버전 관리 (hatchling)

`__init__.py`에서 버전을 관리하고 빌드 시 자동으로 읽어오기:

```toml
# pyproject.toml
[project]
dynamic = ["version"]

[tool.hatch.version]
path = "src/my_package/__init__.py"
```

```python
# src/my_package/__init__.py
__version__ = "1.2.3"
```

##### Git 태그 기반 버전

```toml
[project]
dynamic = ["version"]

[tool.hatch.version]
source = "vcs"

[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"
```

```bash
# Git 태그로 버전 설정
git tag v1.2.3
git push --tags
```

---

### 7. 패키지 구조 체크리스트

프로덕션 수준의 패키지를 만들 때 확인해야 할 항목:

#### 필수 항목

- [ ] `pyproject.toml`에 `[project]` 메타데이터 완성
- [ ] `README.md` 작성 (설치 방법, 사용 예시 포함)
- [ ] `LICENSE` 파일 추가
- [ ] Src layout 사용
- [ ] 테스트 작성 (`tests/` 디렉토리)
- [ ] `.gitignore` 설정

#### 권장 항목

- [ ] `py.typed` 마커 파일 추가 (타입 힌트 지원)
- [ ] CI/CD 파이프라인 구성
- [ ] `CHANGELOG.md` 유지
- [ ] `[project.urls]` 링크 추가
- [ ] Ruff 또는 Black 코드 포맷터 설정
- [ ] mypy 또는 pyright 타입 체크 설정

---

### 8. `setup.py`에서 `pyproject.toml`로 마이그레이션

레거시 프로젝트를 현대적 구조로 마이그레이션하는 방법:

#### 8.1 `setup.py` → `pyproject.toml` 대응

```python
# ❌ 레거시: setup.py
from setuptools import setup, find_packages

setup(
    name="my-package",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.27.0",
        "pydantic>=2.0",
    ],
    python_requires=">=3.11",
)
```

```toml
# ✅ 현대적: pyproject.toml
[project]
name = "my-package"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = [
    "httpx>=0.27.0",
    "pydantic>=2.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

#### 8.2 마이그레이션 단계

1. `setup.py`의 내용을 `pyproject.toml`의 `[project]`로 이전
2. `setup.cfg`가 있다면 해당 내용도 이전
3. `requirements.txt`의 의존성을 `[project.dependencies]`로 이전
4. `[build-system]`을 `hatchling`으로 설정
5. `setup.py`, `setup.cfg` 삭제
6. `MANIFEST.in`이 있다면 `hatchling`의 include/exclude 설정으로 이전

---

## ❓ 자주 묻는 질문 (FAQ)

### Q1: `name`에 하이픈(`-`)과 언더스코어(`_`) 중 어떤 것을 써야 하나요?

**A**: `pyproject.toml`의 `name`에는 **하이픈(`-`)**을 권장합니다. PyPI는 하이픈과 언더스코어를 동일하게 취급합니다(정규화). Python import에서는 하이픈을 언더스코어로 변환합니다.

```
pyproject.toml: name = "my-awesome-package"
PyPI:           my-awesome-package  (또는 my_awesome_package)
import:         import my_awesome_package
```

### Q2: `[project.optional-dependencies]`와 `[dependency-groups]`의 차이는?

**A**:
- **`[project.optional-dependencies]`**: 패키지를 설치하는 사용자가 `pip install my-package[dev]` 형태로 선택하는 추가 의존성
- **`[dependency-groups]`** (PEP 735): 프로젝트 개발 시에만 사용하는 의존성 그룹. 사용자에게 노출되지 않음

```toml
# 사용자가 설치 가능한 extras
[project.optional-dependencies]
postgres = ["psycopg2>=2.9"]

# 개발용 (사용자 미노출)
[dependency-groups]
dev = ["pytest>=8.0", "ruff>=0.8.0"]
```

### Q3: `__init__.py`에 무슨 코드를 넣어야 하나요?

**A**: 최소한의 코드만 넣으세요:

```python
# 권장: 최소한의 내용
"""패키지 설명."""

__version__ = "1.0.0"

# 필요시 편의용 import
from my_package.core import MyClass
```

절대로 무거운 import나 초기화 로직을 넣지 마세요. 패키지를 import하는 것만으로도 부작용이 발생합니다.

### Q4: `py.typed`는 무엇이고 왜 필요한가요?

**A**: `py.typed`는 빈 마커 파일로, 이 패키지가 타입 힌트를 포함하고 있음을 선언합니다.
mypy, pyright 같은 타입 체커가 이 패키지의 타입 정보를 활용합니다.

```
src/my_package/
├── __init__.py
├── core.py
└── py.typed          # 빈 파일. 생성: touch src/my_package/py.typed
```

### Q5: wheel과 sdist의 차이는?

**A**:

| 항목 | wheel (`.whl`) | sdist (`.tar.gz`) |
|------|---------------|------------------|
| 형식 | ZIP 아카이브 | tar.gz 압축 |
| 빌드 | 사전 빌드됨 | 설치 시 빌드 필요 |
| 설치 속도 | 빠름 | 느림 |
| 빌드 도구 필요 | 불필요 | 필요 (setuptools 등) |
| C 확장 | 플랫폼별 빌드 | 설치자가 컴파일 |

> 💡 `uv build`는 기본적으로 wheel과 sdist를 모두 생성합니다.

### Q6: `hatchling`을 선택한 이유는?

**A**: 2026년 기준, hatchling이 가장 현대적이고 실용적인 선택입니다:
- PEP 621 네이티브 지원 (별도 플러그인 불필요)
- 빌드 속도가 빠름
- 소스 배포에 불필요한 파일 자동 제외
- uv, pip-tools 등과 호환 문제가 거의 없음
- 커스텀 빌드 훅 지원

### Q7: 패키지 이름이 다른 패키지와 충돌하면 어떻게 되나요?

**A**: PyPI는 이름의 고유성을 보장합니다 (등록 순서). 사설 인덱스에서는 인덱스 관리자가 관리합니다. **사내 패키지는 회사 네임스페이스**를 사용하여 충돌을 방지하세요:

```
# ❌ 충돌 위험
utils, common, core

# ✅ 네임스페이스 사용
company-utils, company-core, company-auth
```

---

## 🏗️ 예제 프로젝트

| 예제 | 설명 | 핵심 학습 |
|------|------|----------|
| [01-basic-package](./examples/01-basic-package/) | 기본 패키지 구조 (src layout) | pyproject.toml, 빌드, 테스트 |
| [02-namespace-package](./examples/02-namespace-package/) | 네임스페이스 패키지 구성 | implicit namespace, 다중 패키지 |
| [03-private-index](./examples/03-private-index/) | 사설 인덱스 배포 가이드 | uv publish, index 설정 |

각 예제에는 실행 방법이 포함된 `README.md`가 있습니다.

---

## 🔗 참고 자료

- [Python Packaging User Guide](https://packaging.python.org/)
- [PEP 621 — Project metadata](https://peps.python.org/pep-0621/)
- [Hatchling 공식 문서](https://hatch.pypa.io/latest/)
- [Python 네임스페이스 패키지](https://packaging.python.org/en/latest/guides/packaging-namespace-packages/)
- [시맨틱 버전 명세](https://semver.org/lang/ko/)

---

## ⏭️ 다음 강의

[03. OS Independent 개발 방법론 →](../03-os-independent-dev/README.md)
