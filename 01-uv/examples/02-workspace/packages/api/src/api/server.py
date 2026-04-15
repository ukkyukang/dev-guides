"""FastAPI 서버 모듈.

core 패키지의 유틸리티 함수를 사용하여 API를 구성합니다.
이 예제는 워크스페이스에서 패키지 간 의존성이 어떻게 작동하는지 보여줍니다.

실행:
    uv run --package api uvicorn api.server:app --reload
"""

from fastapi import FastAPI

# ✅ 같은 워크스페이스의 core 패키지를 import
from core.utils import add, format_response, get_timestamp

app = FastAPI(
    title="Workspace 예제 API",
    description="uv workspace에서 패키지 간 의존성을 보여주는 API",
    version="0.1.0",
)


@app.get("/")
def root():
    """루트 엔드포인트."""
    return format_response(
        data={"service": "api", "version": "0.1.0"},
        message="API 서버가 정상 작동 중입니다",
    )


@app.get("/health")
def health():
    """헬스 체크 엔드포인트."""
    return {
        "status": "healthy",
        "timestamp": get_timestamp(),
    }


@app.get("/add/{a}/{b}")
def add_numbers(a: int, b: int):
    """두 숫자를 더합니다 (core 패키지의 add 함수 사용).

    Args:
        a: 첫 번째 숫자
        b: 두 번째 숫자
    """
    result = add(a, b)
    return format_response(
        data={"a": a, "b": b, "result": result},
        message="계산 완료",
    )
