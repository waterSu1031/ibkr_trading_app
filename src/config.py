import os, platform
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass

# 운영체제에 따라 .env 파일 자동 선택
PLATFORM = platform.system()
ENV_FILE = ""
if PLATFORM == "Windows": ENV_FILE = ".env.dev"
elif PLATFORM == "Linux": ENV_FILE = ".env.prod"

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ENV_FILE)



@dataclass
class Config:
    # ▶️ 시스템 환경
    MODE: str = os.getenv("MODE", "DEV")
    ENV_FILE: str = ENV_FILE

    # 📁 Base Path 정의
    ROOT_DIR = Path(__file__).resolve().parent.parent  # 프로젝트 루트
    SRC_DIR = ROOT_DIR / "src"
    TRADING_APP_DIR = SRC_DIR / "_trading_app"
    DASHBOARD_APP_DIR = SRC_DIR / "_dashboard_app"

    # 📁 Source Path 정의
    TEMPLATE_DIR = DASHBOARD_APP_DIR / "templates"
    STATIC_DIR = DASHBOARD_APP_DIR / "static"
    DATABASE_DIR = ROOT_DIR / "database" / "sqlite" / "trading.db"

    # 📁 Infra Path 정의
    STORAGE_DIR = ROOT_DIR / "storage"
    LOGS_DIR = STORAGE_DIR / "storage" / "logs"
    REPORTS_DIR = STORAGE_DIR / "trading_records" / "reports"
    SCREENSHOTS_DIR = STORAGE_DIR / "trading_records" / "screenshots"

    # ▶️ IBKR 접속 정보
    IBKR_HOST: str = os.getenv("TRADING_HOST", "localhost")
    IBKR_PORT: int = int(os.getenv("TRADING_PORT", 4002))
    IBKR_CLIENT_ID: int = int(os.getenv("TRADING_CLIENT_ID", 1))

    WEB_HOST: str = os.getenv("WEB_HOST", "localhost")
    WEB_PORT: int = int(os.getenv("WEB_PORT", 8000))

    # ▶️ 데이터베이스, Redis 설정
    SQLITE_URL: str = f"sqlite:///{DATABASE_DIR}"               # SQLite는 파일기반
    MARIA_HOST: str = os.getenv("MARIA_HOST", "localhost")
    MARIA_PORT: int = int(os.getenv("MARIA_PORT", 3306))
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    f"redis://localhost:6379/0"

    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

    # ▶️ 이메일 설정
    REPORT_EMAIL: str = os.getenv("REPORT_EMAIL", "")
    EMAIL_SENDER: str = os.getenv("EMAIL_SENDER", "")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "")
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 25))


    # ▶️ 기타 서비스 예비 슬롯 (확장 가능)
    USE_WEBSOCKET: bool = os.getenv("USE_WEBSOCKET", "true").lower() == "true"
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", 30))

config = Config()