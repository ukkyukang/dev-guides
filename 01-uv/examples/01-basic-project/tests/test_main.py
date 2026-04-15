"""my_app.main 모듈의 테스트."""

from my_app.main import greet


def test_greet_default():
    """greet 함수가 올바른 인사말을 반환하는지 테스트합니다."""
    result = greet("테스트")
    assert "테스트" in result
    assert "환영합니다" in result


def test_greet_with_name():
    """다른 이름으로 greet 함수를 테스트합니다."""
    result = greet("홍길동")
    assert "홍길동" in result
