"""pydantic-settings 기반 앱 설정.

.env 파일과 시스템 환경 변수를 자동으로 읽고 타입 변환/검증합니다.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """앱 설정 — .env 파일과 환경 변수를 자동으로 읽습니다.

    우선순위: 시스템 환경 변수 > .env 파일 > 기본값
    """

    app_name: str = "CrossPlatformDemo"
    debug: bool = False
    port: int = 8501
    database_url: str = "sqlite:///data.db"
    log_level: str = "INFO"
    secret_key: str = "change-me-in-production"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
