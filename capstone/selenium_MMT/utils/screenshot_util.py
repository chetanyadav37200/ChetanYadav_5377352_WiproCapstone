import os
from datetime import datetime
from utils.logger import LogGen

logger = LogGen.loggen()


class ScreenshotUtil:

    @staticmethod
    def capture_screenshot(driver, screenshot_name="screenshot"):
        """
        Captures a local hardware screen image, normalizes file naming conventions,
        and saves it safely inside the reports folder tree structure.
        """
        # Explicit path routing to ensure a nested structure: reports -> screenshots
        screenshot_dir = os.path.join("reports", "screenshots")

        # Guarantee directories exist before saving assets
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        # Build dynamic timestamp format metadata identifiers
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        clean_name = str(screenshot_name).replace(" ", "_")

        # Cross-platform safe path stitching engine
        screenshot_path = os.path.join(screenshot_dir, f"{clean_name}_{timestamp}.png")

        # Command the web browser driver instance to capture frame parameters
        driver.save_screenshot(screenshot_path)
        logger.info(f"Screenshot saved locally at: {screenshot_path}")

        return screenshot_path