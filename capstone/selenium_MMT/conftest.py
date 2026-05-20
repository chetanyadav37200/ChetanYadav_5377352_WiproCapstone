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
    logger.info("Starting Test")
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

    # CRITICAL: Attach the driver instance to the module scope so hooks can find it on failure
    if request.module:
        request.module.driver = driver

    # Waits
    driver.implicitly_wait(implicit_wait)
    driver.maximize_window()


    logger.info(f"Opening URL : {base_url}")
    driver.get(base_url)

    yield driver

    logger.info("Closing Browser")
    driver.quit()
    logger.info("Ending Test")
    logger.info("=======================================")



# AUTO OPEN ALLURE REPORT
def pytest_unconfigure(config):

    print(
        "\n======= TESTS COMPLETED - OPENING ALLURE REPORT ======="
    )

    os.system(
        "allure serve reports/allure-results"
    )