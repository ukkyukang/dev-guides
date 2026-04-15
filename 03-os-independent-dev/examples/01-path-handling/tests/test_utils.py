"""path_demo 유틸리티 테스트."""

from pathlib import Path

from path_demo.utils import (
    find_files,
    get_system_info,
    read_text_safe,
    write_text_safe,
)


def test_write_and_read(tmp_path: Path):
    """UTF-8 파일 쓰기/읽기 테스트."""
    file_path = tmp_path / "subdir" / "test.txt"
    content = "안녕하세요 🌍 Hello World"

    write_text_safe(file_path, content)
    result = read_text_safe(file_path)

    assert result == content
    assert file_path.exists()


def test_find_files(tmp_path: Path):
    """파일 탐색 테스트."""
    (tmp_path / "a.py").write_text("# a", encoding="utf-8")
    (tmp_path / "b.py").write_text("# b", encoding="utf-8")
    (tmp_path / "c.txt").write_text("c", encoding="utf-8")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "d.py").write_text("# d", encoding="utf-8")

    py_files = find_files(tmp_path, "*.py")
    assert len(py_files) == 3


def test_system_info():
    """시스템 정보 반환 테스트."""
    info = get_system_info()
    assert "os" in info
    assert "python" in info
    assert "home" in info
