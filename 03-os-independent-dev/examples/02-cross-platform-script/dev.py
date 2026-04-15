#!/usr/bin/env python3
"""dev.py — 크로스 플랫폼 개발 자동화 스크립트.

OS에 독립적인 개발 명령어를 제공합니다.
Makefile이나 Task 없이도 어떤 OS에서든 동일하게 동작합니다.

Usage:
    uv run python dev.py test      테스트 실행
    uv run python dev.py lint      린트 검사
    uv run python dev.py format    코드 포맷팅
    uv run python dev.py check     lint + test
    uv run python dev.py clean     캐시 정리
    uv run python dev.py info      시스템 정보 출력
"""

from __future__ import annotations

import platform
import shutil
import subprocess
import sys
from pathlib import Path

# 프로젝트 루트
ROOT = Path(__file__).parent


def run(cmd: list[str], cwd: Path = ROOT) -> int:
    """명령어를 실행하고 반환 코드를 돌려줍니다."""
    print(f"\n▶ {' '.join(cmd)}")
    print("-" * 40)
    result = subprocess.run(cmd, cwd=cwd)
    return result.returncode


def cmd_test() -> int:
    """테스트를 실행합니다."""
    return run([sys.executable, "-m", "pytest", "-v"])


def cmd_lint() -> int:
    """린트 검사를 실행합니다."""
    return run([sys.executable, "-m", "ruff", "check", "src/"])


def cmd_format() -> int:
    """코드를 포맷팅합니다."""
    return run([sys.executable, "-m", "ruff", "format", "src/"])


def cmd_check() -> int:
    """린트 + 테스트를 순차적으로 실행합니다."""
    code = cmd_lint()
    if code != 0:
        print("\n❌ 린트 검사 실패!")
        return code

    code = cmd_test()
    if code != 0:
        print("\n❌ 테스트 실패!")
        return code

    print("\n✅ 모든 검사 통과!")
    return 0


def cmd_clean() -> None:
    """빌드 캐시와 임시 파일을 정리합니다."""
    targets = [
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
        ".mypy_cache",
        "dist",
        "*.egg-info",
    ]

    for pattern in targets:
        for path in ROOT.rglob(pattern):
            if path.is_dir():
                print(f"🗑️  {path}")
                shutil.rmtree(path)

    print("✅ 정리 완료!")


def cmd_info() -> None:
    """현재 시스템 정보를 출력합니다."""
    print("🖥️  시스템 정보")
    print(f"  OS:        {platform.system()} {platform.release()}")
    print(f"  Python:    {sys.version}")
    print(f"  실행 파일: {sys.executable}")
    print(f"  CWD:       {Path.cwd()}")
    print(f"  홈:        {Path.home()}")

    # 핵심 도구 확인
    tools = ["git", "uv", "docker", "node"]
    print("\n🔧 도구 상태")
    for tool in tools:
        found = shutil.which(tool)
        status = f"✅ {found}" if found else "❌ 미설치"
        print(f"  {tool:10s}: {status}")


COMMANDS = {
    "test": cmd_test,
    "lint": cmd_lint,
    "format": cmd_format,
    "check": cmd_check,
    "clean": cmd_clean,
    "info": cmd_info,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        print(f"사용 가능한 명령어: {', '.join(COMMANDS.keys())}")
        sys.exit(1)

    result = COMMANDS[sys.argv[1]]()
    if isinstance(result, int) and result != 0:
        sys.exit(result)
