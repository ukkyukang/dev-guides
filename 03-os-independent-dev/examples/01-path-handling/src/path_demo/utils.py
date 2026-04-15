"""크로스 플랫폼 경로 및 파일 처리 유틸리티.

이 모듈은 OS에 독립적인 경로 처리 패턴을 보여줍니다.
모든 함수는 Windows, macOS, Linux에서 동일하게 동작합니다.
"""

from __future__ import annotations

import platform
import tempfile
from pathlib import Path

from platformdirs import user_config_dir, user_data_dir


def get_project_root() -> Path:
    """프로젝트 루트 디렉토리를 반환합니다.

    현재 파일 위치를 기준으로 pyproject.toml이 있는 상위 디렉토리를 탐색합니다.
    """
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "pyproject.toml").exists():
            return current
        current = current.parent
    raise FileNotFoundError("pyproject.toml을 찾을 수 없습니다")


def get_config_path(app_name: str = "path-demo") -> Path:
    """OS에 맞는 설정 파일 경로를 반환합니다.

    - Windows: %APPDATA%/path-demo
    - macOS:   ~/Library/Application Support/path-demo
    - Linux:   ~/.config/path-demo
    """
    config_dir = Path(user_config_dir(app_name))
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_data_path(app_name: str = "path-demo") -> Path:
    """OS에 맞는 데이터 저장 경로를 반환합니다."""
    data_dir = Path(user_data_dir(app_name))
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def read_text_safe(path: Path) -> str:
    """UTF-8로 텍스트 파일을 안전하게 읽습니다.

    인코딩을 명시하여 OS 기본 인코딩(Windows cp949 등) 문제를 방지합니다.
    """
    return path.read_text(encoding="utf-8")


def write_text_safe(path: Path, content: str) -> None:
    """UTF-8로 텍스트 파일을 안전하게 씁니다.

    부모 디렉토리가 없으면 자동 생성합니다.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def find_files(root: Path, pattern: str = "*.py") -> list[Path]:
    """디렉토리에서 패턴에 맞는 파일을 재귀적으로 찾습니다.

    Args:
        root: 검색 시작 디렉토리
        pattern: glob 패턴 (기본: "*.py")

    Returns:
        매칭된 파일 경로 목록 (정렬됨)
    """
    return sorted(root.rglob(pattern))


def get_temp_dir(prefix: str = "path_demo_") -> Path:
    """OS별 임시 디렉토리 안에 전용 임시 디렉토리를 생성합니다."""
    return Path(tempfile.mkdtemp(prefix=prefix))


def get_system_info() -> dict[str, str]:
    """현재 시스템 정보를 반환합니다."""
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "python": platform.python_version(),
        "home": str(Path.home()),
        "cwd": str(Path.cwd()),
        "temp": tempfile.gettempdir(),
    }
