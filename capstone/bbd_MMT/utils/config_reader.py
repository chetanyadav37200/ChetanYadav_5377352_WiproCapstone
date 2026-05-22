import configparser
from utils.logger import LogGen

logger = LogGen.loggen()


class ConfigReader:
    config = configparser.ConfigParser()
    config.read("config/config.ini")

    @staticmethod
    def get_base_url():
        url = ConfigReader.config.get("DEFAULT", "base_url")
        logger.info(f"Base URL fetched : {url}")
        return url

    @staticmethod
    def get_browser():
        browser = ConfigReader.config.get("DEFAULT", "browser")
        logger.info(f"Browser fetched : {browser}")
        return browser

    @staticmethod
    def get_timeout():
        timeout = ConfigReader.config.getint("DEFAULT", "timeout")
        logger.info(f"Timeout fetched : {timeout}")
        return timeout

    @staticmethod
    def get_implicit_wait():
        implicit_wait = ConfigReader.config.getint("DEFAULT", "implicit_wait")
        logger.info(f"Implicit wait fetched : {implicit_wait}")
        return implicit_wait

    @staticmethod
    def get_headless():
        headless = ConfigReader.config.getboolean("DEFAULT", "headless")
        logger.info(f"Headless mode : {headless}")
        return headless

    @classmethod
    def get(cls, key):
        """
        Fallback routing method. Maps generic dict lookups (like .get('browser'))
        to your explicit static methods smoothly.
        """
        key_map = {
            "browser": cls.get_browser,
            "base_url": cls.get_base_url,
            "timeout": cls.get_timeout,
            "implicit_wait": cls.get_implicit_wait,
            "headless": cls.get_headless
        }

        if key in key_map:
            return str(key_map[key]())

        # Fallback for dynamic data entries like mobile_number
        try:
            return cls.config.get("DEFAULT", key)
        except Exception:
            return ""