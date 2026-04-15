# 예제 01: 기본 패키지 구조 (Src Layout)

이 예제는 현대적인 Python 패키지의 기본 구조를 보여줍니다.

## 프로젝트 구조

```
01-basic-package/
├── pyproject.toml
├── LICENSE
├── README.md
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── py.typed          # 타입 힌트 지원 마커
│       ├── core.py           # 핵심 비즈니스 로직
│       └── cli.py            # CLI 엔트리포인트
└── tests/
    ├── test_core.py
    └── test_cli.py
```

## 처음부터 만들어보기

```bash
# 1. 라이브러리 프로젝트 생성
uv init --lib my-package
cd my-package

# 2. 의존성 추가
uv add pydantic
uv add pytest ruff --dev

# 3. 빌드 테스트
uv build

# 4. 테스트 실행
uv run pytest
```

## 준비된 예제 실행하기

```bash
# 1. 의존성 설치
uv sync --all-groups

# 2. 테스트 실행
uv run pytest -v

# 3. CLI 실행
uv run my-cli greet "홍길동"
uv run my-cli version

# 4. 패키지 빌드
uv build
ls dist/

# 5. 코드 포맷 및 린트
uv run ruff check src/
uv run ruff format src/
```

## 주요 학습 포인트

1. **Src Layout**: `src/` 디렉토리로 소스 격리
2. **`pyproject.toml`**: 메타데이터, 의존성, 빌드 시스템, 도구 설정 통합
3. **`[project.scripts]`**: CLI 엔트리포인트 등록
4. **`py.typed`**: 타입 힌트 지원 선언
5. **`uv build`**: wheel과 sdist 생성
