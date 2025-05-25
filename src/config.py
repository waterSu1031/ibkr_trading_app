from pathlib import Path
from dataclasses import dataclass
from typing import List

@dataclass
class TradingConfig:
    # Connection settings
    HOST: str = "127.0.0.1"
    LIVE_PORT: int = 4001
    PAPER_PORT: int = 4002
    CLIENT_ID: int = 1

    # File paths
    BASE_DIR: Path = Path(__file__).parent.parent / "storage"
    LOGS_DIR: Path = BASE_DIR / "logs"
    SCREENSHOTS_DIR: Path = BASE_DIR / "trading_records" / "screenshots"
    REPORTS_DIR: Path = BASE_DIR / "trading_records" / "reports"

    # Ensure directories exist
    def __post_init__(self):
        self.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        self.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        self.REPORTS_DIR.mkdir(parents=True, exist_ok=True)