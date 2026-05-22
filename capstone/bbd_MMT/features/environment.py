import os
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

from utils.config_reader import ConfigReader
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen()


def before_all(context):
    """ Runs once before the entire test suite execution begins. """
    logger.info("=======================================")
    logger.info("Starting BDD Test Execution Suite")

    # Read global configurations from your config util
    context.browser = ConfigReader.get("browser").strip().lower()
    context.base_url = ConfigReader.get("base_url").strip()
    context.implicit_wait = int(ConfigReader.get("implicit_wait"))
    context.timeout = int(ConfigReader.get("timeout"))
    context.headless = ConfigReader.get("headless").strip().lower() == "true"

    logger.info(f"Browser       : {context.browser}")
    logger.info(f"Base URL      : {context.base_url}")
    logger.info(f"Implicit Wait : {context.implicit_wait}")
    logger.info(f"Headless      : {context.headless}")
    logger.info("=======================================")


def before_scenario(context, scenario):
    """ Runs before EVERY individual scenario to isolate browser instances. """
    logger.info(f"--> Initializing browser for Scenario: '{scenario.name}'")

    # CHROME SETUP
    if context.browser == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        if context.headless:
            chrome_options.add_argument("--headless=new")

        context.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )

    # EDGE SETUP
    elif context.browser == "edge":
        edge_options = EdgeOptions()
        edge_options.add_argument("--start-maximized")
        edge_options.add_argument("--disable-notifications")
        edge_options.add_argument("--disable-infobars")
        edge_options.add_argument("--disable-extensions")
        if context.headless:
            edge_options.add_argument("--headless")

        context.driver = webdriver.Edge(options=edge_options)

    # DEFAULT FALLBACK
    else:
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        context.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )

    context.driver.implicitly_wait(context.implicit_wait)
    context.driver.maximize_window()

    logger.info(f"Opening Target URL: {context.base_url}")
    context.driver.get(context.base_url)


def after_scenario(context, scenario):
    """
    Runs immediately after every scenario.
    Captures screenshots on test completion (Pass or Fail) and tears down the browser.
    """
    if hasattr(context, "driver"):
        # Determine status prefix for naming consistency
        status_prefix = "PASSED" if scenario.status == "passed" else "FAILED"

        # Clean scenario name for file saving safety
        clean_scenario_name = (
            scenario.name.replace("[", "_")
            .replace("]", "_")
            .replace("'", "")
            .replace(",", "_")
            .replace(" ", "_")
        )
        screenshot_name = f"{status_prefix}_{clean_scenario_name}"

        try:
            # 1. Attach screenshot to Allure BDD Report
            allure.attach(
                context.driver.get_screenshot_as_png(),
                name=screenshot_name,
                attachment_type=allure.attachment_type.PNG
            )

            # 2. Save a local hardcopy using your custom ScreenshotUtil
            ScreenshotUtil.capture_screenshot(context.driver, screenshot_name=screenshot_name)
            logger.info(f"BDD Automation Engine: Logged milestone snapshot for: {scenario.name} [{status_prefix}]")

        except Exception as e:
            logger.error(f"Global Automation Engine failed to extract scenario screenshot: {str(e)}")

        # Tear down the driver session
        logger.info(f"<-- Tearing Down Browser Session for Scenario: '{scenario.name}'")
        context.driver.quit()


def after_all(context):
    """ Runs once after all feature files finish executing. """
    print("\n-------BDD TESTS COMPLETE! GENERATING AND OPENING ALLURE REPORT--------")
    print("-----------------------------------------------------------------------\n")

    # Automatically compiles and provisions the permanent Allure report dashboard portal
    os.system("allure serve reports/allure-results")