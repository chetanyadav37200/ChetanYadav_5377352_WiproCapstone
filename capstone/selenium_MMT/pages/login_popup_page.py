import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class LoginPopupPage(BasePage):
    # --- Locators ---
    MOBILE_INPUT = (By.CSS_SELECTOR, "input[data-cy='userName']")
    CONTINUE_BTN = (By.CSS_SELECTOR, "button[data-cy='continueBtn']")
    CLOSE_MODAL_BTN = (By.CSS_SELECTOR, "span[data-cy='closeModal']")

    # New locator found in your DOM snapshot for the user consent checkbox
    CONSENT_CHECKBOX = (By.CSS_SELECTOR, "input[data-cy='user-consent-checkbox']")

    def is_login_popup_displayed(self):
        """Checks if the verification popup is visible on screen."""
        return self.is_displayed(self.MOBILE_INPUT)

    def login_with_mobile_and_wait_for_otp(self, mobile_number):
        """Inputs mobile details, checks consent, and clicks Continue."""
        self.logger.info(f"Preparing to enter mobile number: {mobile_number}")

        input_field = self.driver.find_element(*self.MOBILE_INPUT)

        # 1. Click, focus, clear and safely type characters sequentially
        input_field.click()
        input_field.send_keys(Keys.CONTROL + "a")
        input_field.send_keys(Keys.DELETE)

        for digit in str(mobile_number):
            input_field.send_keys(digit)
            time.sleep(0.05)

        input_field.send_keys(Keys.TAB)
        time.sleep(0.5)

        # 2. Handle the mandatory user consent checkbox using JavaScript click
        self.logger.info("Toggling the user-consent checkbox to unlock the form...")
        checkbox_elem = self.driver.find_element(*self.CONSENT_CHECKBOX)
        self.driver.execute_script("arguments[0].click();", checkbox_elem)
        time.sleep(1)  # Allow frontend state calculation to update button

        # 3. Click the newly unlocked Continue button
        self.logger.info("Clicking the Continue button...")
        continue_btn = self.driver.find_element(*self.CONTINUE_BTN)
        self.driver.execute_script("arguments[0].click();", continue_btn)

        # 4. Pause execution loop for physical OTP manual logging entry
        self.logger.info("OTP triggered! Pausing execution loop for 25 seconds for manual OTP entry...")

    def close_popup_if_present(self):
        if self.is_login_popup_displayed():
            self.click(self.CLOSE_MODAL_BTN)