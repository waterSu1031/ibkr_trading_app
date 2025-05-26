from pathlib import Path
from dataclasses import dataclass
from typing import List

@dataclass
class TradingConfig:
    # Connection settings
    def get_config(self):
        return {
            "DASHBOARD": {
                "host": "127.0.0.1",
                "port": 4002,
                "clientId": 1
            },
            "TRADING": {
                "host": "127.0.0.1",
                "port": 4001,
                "clientId": 2
            }
        }

    # File paths
    BASE_DIR: Path = Path(__file__).parent.parent / "storage"
    LOGS_DIR: Path = BASE_DIR / "logs"
    SCREENSHOTS_DIR: Path = BASE_DIR / "trading_records" / "screenshots"
    REPORTS_DIR: Path = BASE_DIR / "trading_records" / "reports"

    # Ensure directories exist
    def make_storage(self):
        self.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        self.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        self.REPORTS_DIR.mkdir(parents=True, exist_ok=True)