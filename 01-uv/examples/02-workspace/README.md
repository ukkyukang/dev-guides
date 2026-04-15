# 예제 02: uv Workspace (모노레포)

이 예제는 `uv workspace`를 사용하여 여러 패키지를 하나의 저장소에서 관리하는 모노레포 구성 방법을 보여줍니다.

## 프로젝트 구조

```
02-workspace/
├── README.md                   # 이 파일
├── pyproject.toml              # 워크스페이스 루트 설정
├── packages/
│   ├── core/                   # 공통 라이브러리
│   │   ├── pyproject.toml
│   │   └── src/core/
│   │       ├── __init__.py
│   │       └── utils.py
│   └── api/                    # API 서버 (core에 의존)
│       ├── pyproject.toml
│       ├── src/api/
│       │   ├── __init__.py
│       │   └── server.py
│       └── tests/
│           └── test_server.py
```

## 핵심 개념

### 왜 Workspace를 사용하는가?

- **코드 공유**: `core` 라이브러리를 `api`에서 직접 import하여 사용
- **단일 Lock 파일**: 모든 패키지의 의존성이 하나의 `uv.lock`으로 관리
- **원자적 변경**: 여러 패키지를 한 커밋으로 수정 가능
- **일관된 버전**: 공통 의존성의 버전이 워크스페이스 전체에서 통일

### Workspace 구성 방법

1. 루트 `pyproject.toml`에 `[tool.uv.workspace]` 섹션 추가
2. 각 멤버 패키지는 자체 `pyproject.toml` 보유
3. 멤버 간 참조는 `[tool.uv.sources]`로 설정

## 처음부터 만들어보기

```bash
# 1. 워크스페이스 루트 생성
mkdir my-monorepo && cd my-monorepo
uv init

# 2. pyproject.toml에 workspace 설정 추가
# [tool.uv.workspace]
# members = ["packages/*"]

# 3. core 패키지 생성
uv init --lib packages/core

# 4. api 패키지 생성
uv init --lib packages/api

# 5. api에서 core 의존성 추가
# packages/api/pyproject.toml에 아래 추가:
# dependencies = ["core"]
# [tool.uv.sources]
# core = { workspace = true }

# 6. 전체 동기화
uv sync
```

## 준비된 예제 실행하기

```bash
# 1. 의존성 설치 (워크스페이스 루트에서)
uv sync

# 2. core 패키지 테스트
uv run python -c "from core.utils import add; print(add(1, 2))"

# 3. api 서버 실행
uv run --package api python -m api

# 4. api 테스트 실행
uv run --package api pytest
```

## 주요 학습 포인트

1. **`[tool.uv.workspace]`**: 워크스페이스 멤버 정의
2. **`{ workspace = true }`**: 멤버 간 의존성 연결
3. **`uv run --package`**: 특정 패키지 컨텍스트에서 실행
4. **단일 Lock 파일**: 워크스페이스 전체의 의존성 일관성 보장
5. **자동 editable 설치**: `core`를 수정하면 `api`에 즉시 반영
