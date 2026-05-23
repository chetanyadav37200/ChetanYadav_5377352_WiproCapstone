import time
import os
import allure

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
    context.driver = Driver(
        uc=True
    )

    context.driver.maximize_window()

    context.driver.implicitly_wait(
        ConfigReader.get_implicit_wait()
    )

    # OPEN WEBSITE
    base_url = "https://www.makemytrip.com/"

    logger.info(
        f"OPENING MAKEMYTRIP WEBSITE: {base_url}"
    )

    context.driver.get(
        base_url
    )

    # WAF WAIT
    time.sleep(2)

    logger.info(
        f"CURRENT URL: {context.driver.current_url}"
    )


def after_step(context, step):

    try:

        # CAPTURE SCREENSHOT FOR EVERY STEP
        path = ScreenshotUtil.capture_screenshot(
            context.driver,
            f"{step.status}_{step.name[:20]}"
        )

        # ATTACH SCREENSHOT TO ALLURE REPORT
        allure.attach.file(
            path,
            name=f"{step.status.upper()} - {step.name}",
            attachment_type=allure.attachment_type.PNG
        )

        if step.status == "failed":

            logger.error(
                f"STEP FAILED: {step.name}"
            )

        elif step.status == "passed":

            logger.info(
                f"STEP PASSED: {step.name}"
            )

    except Exception as e:

        logger.error(
            f"SCREENSHOT FAILED: {str(e)}"
        )


def after_scenario(context, scenario):

    logger.info(
        f"========== CLOSING SCENARIO: {scenario.name} =========="
    )

    if hasattr(context, 'driver'):

        try:

            with open("logs/automation.log", "r") as log_file:

                allure.attach(
                    log_file.read(),
                    name="Execution Logs",
                    attachment_type=allure.attachment_type.TEXT
                )

            context.driver.quit()

            logger.info(
                "BROWSER CLOSED SUCCESSFULLY"
            )

        except Exception as e:

            logger.error(
                f"ERROR CLOSING BROWSER: {str(e)}"
            )


def after_all(context):

    print(
        "\n======= TESTS COMPLETED - OPENING ALLURE REPORT ======="
    )

    os.system(
        "allure generate reports/allure-results -o reports/allure-report --clean"
    )

    os.system(
        "allure open reports/allure-report"
    )