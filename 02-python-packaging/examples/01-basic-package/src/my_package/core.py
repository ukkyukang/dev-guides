"""핵심 비즈니스 로직 모듈.

이 모듈은 패키지의 핵심 데이터 모델과 비즈니스 로직을 담고 있습니다.
Pydantic을 사용하여 데이터 검증을 수행합니다.
"""

from pydantic import BaseModel, EmailStr, field_validator


class User(BaseModel):
    """사용자 모델.

    Attributes:
        name: 사용자 이름
        email: 이메일 주소
        role: 역할 (기본값: "member")

    Example:
        >>> user = User(name="홍길동", email="gildong@example.com")
        >>> user.display_name
        '홍길동 <gildong@example.com>'
    """

    name: str
    email: str
    role: str = "member"

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        """이름이 비어있지 않은지 검증합니다."""
        if not v.strip():
            raise ValueError("이름은 비어있을 수 없습니다")
        return v.strip()

    @property
    def display_name(self) -> str:
        """표시용 이름을 반환합니다."""
        return f"{self.name} <{self.email}>"


class Config(BaseModel):
    """애플리케이션 설정 모델.

    Attributes:
        app_name: 애플리케이션 이름
        debug: 디버그 모드 여부
        max_retries: 최대 재시도 횟수
    """

    app_name: str = "my-app"
    debug: bool = False
    max_retries: int = 3

    @field_validator("max_retries")
    @classmethod
    def max_retries_must_be_positive(cls, v: int) -> int:
        """최대 재시도 횟수는 양수여야 합니다."""
        if v < 0:
            raise ValueError("max_retries는 0 이상이어야 합니다")
        return v


def create_user(name: str, email: str, role: str = "member") -> User:
    """새 사용자를 생성합니다.

    Args:
        name: 사용자 이름
        email: 이메일 주소
        role: 역할 (기본값: "member")

    Returns:
        생성된 User 객체

    Raises:
        ValueError: 이름이 비어있거나 유효하지 않은 경우
    """
    return User(name=name, email=email, role=role)


def get_users_by_role(users: list[User], role: str) -> list[User]:
    """특정 역할의 사용자 목록을 반환합니다.

    Args:
        users: 전체 사용자 목록
        role: 필터링할 역할

    Returns:
        해당 역할의 사용자 목록
    """
    return [user for user in users if user.role == role]
