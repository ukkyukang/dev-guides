"""core 모듈 테스트."""

import pytest

from my_package.core import Config, User, create_user, get_users_by_role


class TestUser:
    """User 모델 테스트."""

    def test_create_user(self):
        """기본 사용자 생성."""
        user = User(name="홍길동", email="gildong@example.com")
        assert user.name == "홍길동"
        assert user.email == "gildong@example.com"
        assert user.role == "member"

    def test_display_name(self):
        """display_name 프로퍼티."""
        user = User(name="홍길동", email="gildong@example.com")
        assert user.display_name == "홍길동 <gildong@example.com>"

    def test_name_stripped(self):
        """이름 앞뒤 공백 제거."""
        user = User(name="  홍길동  ", email="gildong@example.com")
        assert user.name == "홍길동"

    def test_empty_name_raises(self):
        """빈 이름은 ValueError."""
        with pytest.raises(ValueError, match="비어있을 수 없습니다"):
            User(name="   ", email="gildong@example.com")

    def test_custom_role(self):
        """사용자 역할 지정."""
        user = User(name="관리자", email="admin@example.com", role="admin")
        assert user.role == "admin"


class TestConfig:
    """Config 모델 테스트."""

    def test_default_config(self):
        """기본 설정값."""
        config = Config()
        assert config.app_name == "my-app"
        assert config.debug is False
        assert config.max_retries == 3

    def test_custom_config(self):
        """커스텀 설정값."""
        config = Config(app_name="custom", debug=True, max_retries=5)
        assert config.app_name == "custom"
        assert config.debug is True

    def test_negative_retries_raises(self):
        """음수 재시도 횟수는 ValueError."""
        with pytest.raises(ValueError, match="0 이상"):
            Config(max_retries=-1)


class TestFunctions:
    """유틸리티 함수 테스트."""

    def test_create_user_function(self):
        """create_user 헬퍼 함수."""
        user = create_user("테스트", "test@example.com")
        assert isinstance(user, User)
        assert user.name == "테스트"

    def test_get_users_by_role(self):
        """역할별 사용자 필터링."""
        users = [
            User(name="홍길동", email="a@b.com", role="admin"),
            User(name="김철수", email="c@d.com", role="member"),
            User(name="이영희", email="e@f.com", role="admin"),
        ]
        admins = get_users_by_role(users, "admin")
        assert len(admins) == 2
        assert all(u.role == "admin" for u in admins)

    def test_get_users_by_role_empty(self):
        """존재하지 않는 역할 필터링."""
        users = [User(name="홍길동", email="a@b.com", role="member")]
        result = get_users_by_role(users, "admin")
        assert result == []
