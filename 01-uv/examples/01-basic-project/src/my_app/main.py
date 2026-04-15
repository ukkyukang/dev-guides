"""메인 애플리케이션 모듈.

이 모듈은 httpx를 사용하여 간단한 HTTP 요청을 수행하는 예제입니다.
`uv run python -m my_app` 으로 실행할 수 있습니다.
"""

import httpx


def fetch_ip_info() -> dict:
    """공개 API를 호출하여 현재 IP 정보를 가져옵니다.

    Returns:
        dict: IP 주소 정보를 담은 딕셔너리

    Example:
        >>> info = fetch_ip_info()
        >>> print(info["ip"])
        203.0.113.1
    """
    response = httpx.get("https://httpbin.org/ip")
    response.raise_for_status()
    return response.json()


def greet(name: str) -> str:
    """인사말을 생성합니다.

    Args:
        name: 인사 대상의 이름

    Returns:
        인사말 문자열
    """
    return f"안녕하세요, {name}님! uv 프로젝트에 오신 것을 환영합니다 🚀"


def main() -> None:
    """메인 진입점."""
    print("=" * 50)
    print("🐍 uv 기본 프로젝트 예제")
    print("=" * 50)

    # 인사말 출력
    print(greet("개발자"))
    print()

    # HTTP 요청 예제
    print("📡 현재 IP 정보를 가져오는 중...")
    try:
        info = fetch_ip_info()
        print(f"✅ 현재 IP: {info.get('origin', '알 수 없음')}")
    except httpx.HTTPError as e:
        print(f"❌ 요청 실패: {e}")

    print()
    print("🎉 예제 실행 완료!")


if __name__ == "__main__":
    main()
