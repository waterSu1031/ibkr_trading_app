from pydantic import BaseModel, Field
import os
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass, field
from typing import List

# .env 파일 로딩
load_dotenv(dotenv_path=os.getenv("ENV_FILE", ".env"))


@dataclass
class TradingConfig:
    # 실행 환경
    MODE: str = os.getenv("MODE", "development")

    # IBKR 연결 정보
    TRADING_HOST: str = os.getenv("TRADING_HOST", "127.0.0.1")
    TRADING_PORT: int = int(os.getenv("TRADING_PORT", 4001))
    TRADING_CLIENT_ID: int = int(os.getenv("TRADING_CLIENT_ID", 2))

    DASHBOARD_HOST: str = os.getenv("DASHBOARD_HOST", "127.0.0.1")
    DASHBOARD_PORT: int = int(os.getenv("DASHBOARD_PORT", 4002))
    DASHBOARD_CLIENT_ID: int = int(os.getenv("DASHBOARD_CLIENT_ID", 1))

    # 디렉토리
    BASE_DIR: Path = Path(__file__).resolve().parent.parent / "storage"
    LOGS_DIR: Path = BASE_DIR / "logs"
    REPORTS_DIR: Path = BASE_DIR / "trading_records" / "reports"
    SCREENSHOTS_DIR: Path = BASE_DIR / "trading_records" / "screenshots"

    # 이메일
    REPORT_EMAIL: str = os.getenv("REPORT_EMAIL", "")
    EMAIL_SENDER: str = os.getenv("EMAIL_SENDER", "")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "")
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))


# 인스턴스 생성
config = TradingConfig()



# pip install pydantic-settings
# from pydantic_settings import BaseSettings
# from pathlib import Path

# class TradingConfig(BaseSettings):
#     MODE: str = "development"
#     TRADING_HOST: str = "127.0.0.1"
#     TRADING_PORT: int = 4001
#     TRADING_CLIENT_ID: int = 2
#
#     DASHBOARD_HOST: str = "127.0.0.1"
#     DASHBOARD_PORT: int = 4002
#     DASHBOARD_CLIENT_ID: int = 1
#
#     REPORT_EMAIL: str = ""
#     EMAIL_SENDER: str = ""
#     EMAIL_PASSWORD: str = ""
#     SMTP_SERVER: str = ""
#     SMTP_PORT: int = 587
#
#     BASE_DIR: Path = Path(__file__).resolve().parent.parent / "storage"
#     LOGS_DIR: Path = BASE_DIR / "logs"
#     REPORTS_DIR: Path = BASE_DIR / "trading_records" / "reports"
#     SCREENSHOTS_DIR: Path = BASE_DIR / "trading_records" / "screenshots"