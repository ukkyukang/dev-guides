"""CLI 모듈 테스트."""

from unittest.mock import patch

from my_package.cli import cmd_config, cmd_version


def test_version_output(capsys):
    """version 명령어 출력 테스트."""
    # argparse.Namespace를 모방
    class Args:
        pass

    cmd_version(Args())
    captured = capsys.readouterr()
    assert "my-package v" in captured.out
    assert "1.0.0" in captured.out


def test_config_output(capsys):
    """config 명령어 출력 테스트."""

    class Args:
        pass

    cmd_config(Args())
    captured = capsys.readouterr()
    assert "my-app" in captured.out
    assert "기본 설정" in captured.out
