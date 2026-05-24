import time
import os
import allure
import re

from seleniumbase import Driver

from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
from utils.config_reader import ConfigReader

logger = LogGen.loggen()


def before_scenario(context, scenario):
    logger.info(
        f"========== STARTING SCENARIO: {scenario.name} =========="
    )

    # USING SELENIUMBASE UC MODE
    context.driver = Driver(uc=True)
    context.driver.maximize_window()
    context.driver.implicitly_wait(ConfigReader.get_implicit_wait())

    # OPEN WEBSITE
    base_url = "https://www.makemytrip.com/"
    logger.info(f"OPENING MAKEMYTRIP WEBSITE: {base_url}")
    context.driver.get(base_url)

    # WAF WAIT
    time.sleep(2)
    logger.info(f"CURRENT URL: {context.driver.current_url}")


def after_step(context, step):
    # Safe check: If the driver didn't load or crashed, don't try to take a screenshot
    driver = getattr(context, 'driver', None)
    if driver is None:
        logger.warning(f"Skipping screenshot hook: Driver context is missing for step '{step.name}'")
        return

    try:
        # CRITICAL FIX: Sanitize the file name string to strip out illegal filename character artifacts
        # This replaces any non-alphanumeric characters with underscores
        safe_step_name = re.sub(r'[^a-zA-Z0-9_]', '_', step.name[:20].strip())
        screenshot_filename = f"{step.status}_{safe_step_name}"

        # CAPTURE SCREENSHOT FOR EVERY STEP
        path = ScreenshotUtil.capture_screenshot(context.driver, screenshot_filename)

        # SEAMLESS ATTACHMENT VALIDATION
        if path and os.path.exists(path):
            allure.attach.file(
                path,
                name=f"{step.status.upper()} - {step.name}",
                attachment_type=allure.attachment_type.PNG
            )
        else:
            logger.warning(f"Screenshot utility path invalid or unreadable: {path}")

        # Logging metrics
        if step.status == "failed":
            logger.error(f"STEP FAILED: {step.name}")
        elif step.status == "passed":
            logger.info(f"STEP PASSED: {step.name}")

    except Exception as e:
        logger.error(f"ALLURE SCREENSHOT ATTACHMENT HOOK FAILED: {str(e)}")


def after_scenario(context, scenario):
    logger.info(
        f"========== CLOSING SCENARIO: {scenario.name} =========="
    )

    if hasattr(context, 'driver'):
        try:
            # Safe log file binding check
            log_path = "logs/automation.log"
            if os.path.exists(log_path):
                with open(log_path, "r") as log_file:
                    allure.attach(
                        log_file.read(),
                        name="Execution Logs",
                        attachment_type=allure.attachment_type.TEXT
                    )

            context.driver.quit()
            logger.info("BROWSER CLOSED SUCCESSFULLY")

        except Exception as e:
            logger.error(f"ERROR CLOSING BROWSER: {str(e)}")


def after_all(context):
    print("\n======= TESTS COMPLETED - GENERATING ALLURE REPORT =======")

    # Generate the static report cleanly
    os.system("allure generate reports/allure-results -o reports/allure-report --clean")

    # Note: Running 'allure open' starts an endless web server loop.
    # If your runtests.py hangs because of this, replace this with printing the instructions instead!
    os.system("allure open reports/allure-report")