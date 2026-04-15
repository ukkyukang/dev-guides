"""공통 유틸리티 함수 모음.

이 모듈은 워크스페이스 내 다른 패키지에서 공유하는 유틸리티를 제공합니다.
"""

from datetime import datetime, timezone


def add(a: int | float, b: int | float) -> int | float:
    """두 숫자를 더합니다.

    Args:
        a: 첫 번째 숫자
        b: 두 번째 숫자

    Returns:
        두 숫자의 합

    Example:
        >>> add(1, 2)
        3
    """
    return a + b


def get_timestamp() -> str:
    """현재 UTC 타임스탬프를 ISO 형식으로 반환합니다.

    Returns:
        ISO 8601 형식의 UTC 타임스탬프 문자열

    Example:
        >>> get_timestamp()
        '2026-01-15T09:30:00+00:00'
    """
    return datetime.now(timezone.utc).isoformat()


def format_response(data: dict, message: str = "success") -> dict:
    """API 응답을 표준 형식으로 감쌉니다.

    Args:
        data: 응답 데이터
        message: 응답 메시지 (기본값: "success")

    Returns:
        표준화된 응답 딕셔너리

    Example:
        >>> format_response({"name": "test"})
        {'status': 'success', 'message': 'success', 'data': {'name': 'test'}, 'timestamp': '...'}
    """
    return {
        "status": "success",
        "message": message,
        "data": data,
        "timestamp": get_timestamp(),
    }
