# pages/home_page.py

from pages.base_page import BasePage
from locators.home_locators import HomePageLocators


class HomePage(BasePage):

    def dismiss_login_if_present(self):
        self.logger.info("Checking for overlay login prompts...")
        if self.is_displayed(HomePageLocators.CLOSE_LOGIN_MODAL):
            self.click(HomePageLocators.CLOSE_LOGIN_MODAL)
            self.logger.info("Login modal dismissed.")

    def click_travel_insurance(self):
        self.logger.info("Navigating to Travel Insurance page...")
        self.click(HomePageLocators.TRAVEL_INSURANCE_TAB)