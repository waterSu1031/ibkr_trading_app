from datetime import datetime
from pathlib import Path
from typing import Optional
import pyautogui, logging
from src.config import config  # Updated import path

logger = logging.getLogger(__name__)

class Screenshotter:
    def __init__(self):
        self.config = config

    def capture(self, symbol: str) -> Optional[Path]:
        """
        Capture screenshot of _web_app activity
        Returns the path to the saved screenshot
        """
        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{symbol}_{timestamp}.png"
            filepath = self.config.SCREENSHOTS_DIR / filename

            # Take screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save(str(filepath))

            return filepath

        except Exception as e:
            logger.warning(f"Error capturing screenshot: {str(e)}")
            return None

    def capture_region(self, symbol: str, region: tuple) -> Optional[Path]:
        """
        Capture screenshot of specific region (x, y, width, height)
        Returns the path to the saved screenshot
        """
        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{symbol}_{timestamp}_region.png"
            filepath = self.config.SCREENSHOTS_DIR / filename

            # Take screenshot of specific region
            screenshot = pyautogui.screenshot(region=region)
            screenshot.save(str(filepath))

            return filepath

        except Exception as e:
            logger.warning(f"Error capturing region screenshot: {str(e)}")
            return None