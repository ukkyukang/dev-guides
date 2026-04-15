"""my_package — Python 패키징 기본 예제.

이 패키지는 현대적인 Python 패키지 구조를 보여주는 교육용 예제입니다.

Example:
    >>> from my_package import __version__
    >>> print(__version__)
    1.0.0

    >>> from my_package.core import User
    >>> user = User(name="홍길동", email="gildong@example.com")
    >>> print(user.display_name)
    홍길동 <gildong@example.com>
"""

__version__ = "1.0.0"
