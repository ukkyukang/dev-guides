# 예제 01: 기본 uv 프로젝트

이 예제는 `uv`를 사용하여 기본적인 Python 프로젝트를 생성하고 관리하는 방법을 보여줍니다.

## 프로젝트 구조

```
01-basic-project/
├── README.md              # 이 파일
├── pyproject.toml          # 프로젝트 설정 및 의존성
├── src/
│   └── my_app/
│       ├── __init__.py
│       └── main.py         # 메인 애플리케이션
└── tests/
    └── test_main.py        # 테스트
```

## 처음부터 만들어보기

이 예제를 직접 처음부터 만들고 싶다면:

```bash
# 1. 프로젝트 생성
uv init --lib my-app
cd my-app

# 2. 의존성 추가
uv add httpx
uv add pytest --dev

# 3. 실행
uv run python -m my_app
```

## 준비된 예제 실행하기

```bash
# 1. 의존성 설치
uv sync

# 2. 앱 실행
uv run python -m my_app

# 3. 테스트 실행
uv run pytest
```

## 주요 학습 포인트

1. **`uv init`**: 프로젝트 스캐폴딩
2. **`uv add`**: 의존성 추가 및 `pyproject.toml` + `uv.lock` 자동 업데이트
3. **`uv sync`**: Lock 파일 기반 의존성 설치
4. **`uv run`**: 가상 환경 안에서 명령 실행 (자동 활성화)
5. **`src/` 레이아웃**: 현대적 Python 프로젝트 구조
