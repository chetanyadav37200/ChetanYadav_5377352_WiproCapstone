# conftest.py

import pytest
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


@pytest.fixture(scope="module")
def driver(request):
    # Read configuration
    browser = ConfigReader.get("browser").strip().lower()
    base_url = ConfigReader.get("base_url").strip()
    implicit_wait = int(ConfigReader.get("implicit_wait"))
    timeout = int(ConfigReader.get("timeout"))
    headless = ConfigReader.get("headless").strip().lower() == "true"

    logger.info("=======================================")
    logger.info("Starting Test Execution Suite")
    logger.info(f"Browser : {browser}")
    logger.info(f"Base URL : {base_url}")
    logger.info(f"Implicit Wait : {implicit_wait}")
    logger.info(f"Timeout : {timeout}")
    logger.info(f"Headless : {headless}")

    # CHROME
    if browser == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")

        if headless:
            chrome_options.add_argument("--headless=new")

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )

    # EDGE
    elif browser == "edge":
        edge_options = EdgeOptions()
        edge_options.add_argument("--start-maximized")
        edge_options.add_argument("--disable-notifications")
        edge_options.add_argument("--disable-infobars")
        edge_options.add_argument("--disable-extensions")

        if headless:
            edge_options.add_argument("--headless")

        driver = webdriver.Edge(options=edge_options)

    # DEFAULT CHROME
    else:
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )

    # CRITICAL: Attach driver to the module scope so hooks can track down instances on execution
    if request.module:
        request.module.driver = driver

    # Window Management & Initial Launch Setup
    driver.implicitly_wait(implicit_wait)
    driver.maximize_window()

    logger.info(f"Opening Target URL : {base_url}")
    driver.get(base_url)

    yield driver

    logger.info("Tearing Down Browser Session")
    driver.quit()
    logger.info("Test Run Concluded")
    logger.info("=======================================")


# COMPILE AND OPEN PERMANENT ALLURE REPORT PORTAL
def pytest_unconfigure(config):
    """
    This built-in Pytest hook runs exactly once after
    all tests have finished and the browsers are closed.
    """
    print("-------TESTS COMPLETE! GENERATING AND OPENING ALLURE REPORT--------")
    print("-------------------------------------------------------\n")

    # Automatically triggers the terminal command to open the report
    os.system("allure serve reports/allure-results") ,


# ==================================================================================
#  GLOBAL SCREENSHOT HOOK (RUNS ON EVERY COMPLETED TEST CASE - PASS OR FAIL)
# ==================================================================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture a screenshot globally on EVERY test completion (Pass or Fail),
    attaching it to both Allure reports and using your custom local ScreenshotUtil.
    """
    outcome = yield
    report = outcome.get_result()

    # Intercept only during the operational test call footprint phrase
    if report.when == "call":
        driver = None

        # Mine the active selenium web application interface hook
        if hasattr(item.module, "driver"):
            driver = item.module.driver
        elif "driver" in item.funcargs:
            driver = item.funcargs["driver"]

        if driver:
            # Clean parameter characters out of parameterized names for safe system strings
            clean_test_name = (
                item.name.replace("[", "_")
                .replace("]", "_")
                .replace("'", "")
                .replace(",", "_")
                .replace(" ", "_")
            )

            # Label with appropriate status strings
            status_prefix = "PASSED" if report.passed else "FAILED"
            screenshot_name = f"{status_prefix}_{clean_test_name}"

            try:
                # 1. Store inside permanent allure data reports folder
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=screenshot_name,
                    attachment_type=allure.attachment_type.PNG
                )

                # 2. Maintain local workspace file asset copy for offline references
                ScreenshotUtil.capture_screenshot(driver, screenshot_name=screenshot_name)
                logger.info(f"Global Automation Engine: Logged milestone snapshot for: {item.name} [{status_prefix}]")

            except Exception as e:
                logger.error(f"Global Automation Engine Failed to execute screen snapshot logic: {str(e)}")