from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    CLOSE_LOGIN_MODAL = (By.CSS_SELECTOR, "span[data-cy='closeModal']")
    TRAVEL_INSURANCE_TAB = (By.CSS_SELECTOR, "li[data-cy='menu_TravelInsurance']")

    def dismiss_login_if_present(self):
        self.logger.info("Checking for overlay login prompts...")
        if self.is_displayed(self.CLOSE_LOGIN_MODAL):
            self.click(self.CLOSE_LOGIN_MODAL)
            self.logger.info("Login modal dismissed.")

    def click_travel_insurance(self):
        self.logger.info("Navigating to Travel Insurance page...")
        self.click(self.TRAVEL_INSURANCE_TAB)