# pages/login_popup_page.py

import time
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from locators.login_popup_locators import LoginPopupLocators


class LoginPopupPage(BasePage):

    def is_login_popup_displayed(self):
        """Checks if the verification popup is visible on screen."""
        return self.is_displayed(LoginPopupLocators.MOBILE_INPUT)

    def login_with_mobile_and_wait_for_otp(self, mobile_number):
        """Inputs mobile details, checks consent, and clicks Continue."""
        self.logger.info(f"Preparing to enter mobile number: {mobile_number}")

        input_field = self.driver.find_element(*LoginPopupLocators.MOBILE_INPUT)

        input_field.click()
        input_field.send_keys(Keys.CONTROL + "a")
        input_field.send_keys(Keys.DELETE)

        for digit in str(mobile_number):
            input_field.send_keys(digit)
            time.sleep(0.05)

        input_field.send_keys(Keys.TAB)
        time.sleep(0.5)

        self.logger.info("Toggling the user-consent checkbox to unlock the form...")
        checkbox_elem = self.driver.find_element(*LoginPopupLocators.CONSENT_CHECKBOX)
        self.driver.execute_script("arguments[0].click();", checkbox_elem)
        time.sleep(1)

        self.logger.info("Clicking the Continue button...")
        continue_btn = self.driver.find_element(*LoginPopupLocators.CONTINUE_BTN)
        self.driver.execute_script("arguments[0].click();", continue_btn)

        self.logger.info("OTP triggered! Pausing execution loop for 25 seconds for manual OTP entry...")

    def close_popup_if_present(self):
        if self.is_login_popup_displayed():
            self.click(LoginPopupLocators.CLOSE_MODAL_BTN)