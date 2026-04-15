"""CLI 엔트리포인트 모듈.

이 모듈은 [project.scripts]를 통해 등록된 CLI 명령어의 진입점입니다.
설치 후 터미널에서 `my-cli` 명령어로 실행할 수 있습니다.

Usage:
    my-cli greet "홍길동"
    my-cli version
    my-cli config
"""

import argparse
import sys

from my_package import __version__
from my_package.core import Config, create_user


def cmd_greet(args: argparse.Namespace) -> None:
    """인사 명령어."""
    user = create_user(name=args.name, email=f"{args.name}@example.com")
    print(f"👋 {user.display_name}")
    print(f"   역할: {user.role}")


def cmd_version(args: argparse.Namespace) -> None:
    """버전 출력 명령어."""
    print(f"my-package v{__version__}")


def cmd_config(args: argparse.Namespace) -> None:
    """기본 설정 출력 명령어."""
    config = Config()
    print("⚙️  기본 설정:")
    print(f"   앱 이름: {config.app_name}")
    print(f"   디버그 모드: {config.debug}")
    print(f"   최대 재시도: {config.max_retries}")


def main() -> None:
    """CLI 메인 진입점.

    이 함수가 pyproject.toml의 [project.scripts]에 등록됩니다:
        my-cli = "my_package.cli:main"
    """
    parser = argparse.ArgumentParser(
        prog="my-cli",
        description="Python 패키징 예제 CLI 도구",
    )
    subparsers = parser.add_subparsers(dest="command", help="사용 가능한 명령어")

    # greet 명령어
    greet_parser = subparsers.add_parser("greet", help="사용자에게 인사합니다")
    greet_parser.add_argument("name", help="인사할 사용자 이름")
    greet_parser.set_defaults(func=cmd_greet)

    # version 명령어
    version_parser = subparsers.add_parser("version", help="버전을 출력합니다")
    version_parser.set_defaults(func=cmd_version)

    # config 명령어
    config_parser = subparsers.add_parser("config", help="기본 설정을 출력합니다")
    config_parser.set_defaults(func=cmd_config)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
