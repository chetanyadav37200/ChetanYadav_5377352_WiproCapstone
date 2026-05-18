from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class PlansPage(BasePage):
    CHOOSE_PLAN_HEADER = (By.CSS_SELECTOR, "div[data-test-id='Header-HeaderWrapper']")

    FIRST_PLAN_CARD = (By.CSS_SELECTOR, "div[data-test-id='Card-CardWrapper']")

    BUY_NOW_BTN = (By.XPATH,
                   "//div[@data-test-id='Card-CardWrapper'][1]//button[descendant-or-self::*[normalize-space(text())='BUY NOW']]")

    def is_choose_plan_present(self):
        self.logger.info("Checking if Choose Your Plan layout has rendered...")
        return self.is_displayed(self.CHOOSE_PLAN_HEADER)

    def click_buy_now(self):
        self.logger.info("Selecting the first available insurance plan via 'BUY NOW' hook...")
        self.click(self.BUY_NOW_BTN)