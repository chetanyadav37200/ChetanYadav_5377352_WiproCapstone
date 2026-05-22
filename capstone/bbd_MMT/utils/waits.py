# utils/waits.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from utils.config_reader import ConfigReader
from utils.logger import LogGen

logger = LogGen.loggen()

class WaitUtils:

    @staticmethod
    def _get_default_timeout():
        """Helper to safely fetch timeout configurations dynamically without crashing."""
        try:
            # Resolves the dictionary reader get key seamlessly
            config_val = ConfigReader.get("timeout")
            return int(config_val) if config_val else 15
        except Exception:
            return 15  # Secure fallback structural default boundary

    @staticmethod
    def wait_for_element_visible(driver, locator, timeout=None):
        if timeout is None:
            timeout = WaitUtils._get_default_timeout()
        try:
            logger.info(f"Waiting for element visibility: {locator}")
            return WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"Timeout waiting for visibility: {locator}")
            raise

    @staticmethod
    def wait_for_element_clickable(driver, locator, timeout=None):
        if timeout is None:
            timeout = WaitUtils._get_default_timeout()
        try:
            logger.info(f"Waiting for element clickable: {locator}")
            return WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            logger.error(f"Timeout waiting for clickable: {locator}")
            raise

    @staticmethod
    def wait_for_presence_of_element(driver, locator, timeout=None):
        if timeout is None:
            timeout = WaitUtils._get_default_timeout()
        try:
            logger.info(f"Waiting for element presence: {locator}")
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"Timeout waiting for presence: {locator}")
            raise

    @staticmethod
    def wait_for_title_contains(driver, title, timeout=None):
        if timeout is None:
            timeout = WaitUtils._get_default_timeout()
        try:
            logger.info(f"Waiting for title contains: {title}")
            return WebDriverWait(driver, timeout).until(
                EC.title_contains(title)
            )
        except TimeoutException:
            logger.error(f"Timeout waiting for title: {title}")
            raise

    @staticmethod
    def wait_for_alert(driver, timeout=None):
        if timeout is None:
            timeout = WaitUtils._get_default_timeout()
        try:
            logger.info("Waiting for alert")
            return WebDriverWait(driver, timeout).until(
                EC.alert_is_present()
            )
        except TimeoutException:
            logger.error("Timeout waiting for alert")
            raise

    @staticmethod
    def wait_for_invisibility(driver, locator, timeout=None):
        if timeout is None:
            timeout = WaitUtils._get_default_timeout()
        try:
            logger.info(f"Waiting for invisibility: {locator}")
            return WebDriverWait(driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"Timeout waiting for invisibility: {locator}")
            raise