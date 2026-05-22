# pages/traveller_page.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from locators.traveller_locators import TravellerPageLocators
from utils.waits import WaitUtils


class TravellerPage(BasePage):

    def is_traveller_page_open(self):
        """Dynamically waits for the checkout traveler screen to finish initializing."""
        self.logger.info("Waiting explicitly for checkout form containers to mount...")
        try:
            element = WaitUtils.wait_for_element_visible(self.driver, TravellerPageLocators.TRAVELLER_PAGE_CHECKMARK)
            return element.is_displayed()
        except Exception:
            return False

    def is_traveller_header_present(self):
        """Validates if the header block layout component is cleanly rendered on screen."""
        try:
            element = WaitUtils.wait_for_presence_of_element(self.driver, TravellerPageLocators.TRAVELLER_PAGE_CHECKMARK)
            return element.is_displayed()
        except Exception:
            return False

    def _safe_clear_and_type(self, locator, text_value):
        """
        Ensures input fields accurately register data inside single-page React environments.
        Bypasses layout intercepts, cleans the target, types input text,
        and explicitly emulates a TAB key press to blur focus and trigger frontend event validations.
        """
        element = WaitUtils.wait_for_element_visible(self.driver, locator)

        # Center target element on screen to drop focus cleanly
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.driver.execute_script("arguments[0].click();", element)

        # Clear fields natively via structural keyboard emulations
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACKSPACE)

        # Type value character-by-character to guarantee state binding registration
        for char in str(text_value):
            element.send_keys(char)
            time.sleep(0.02)  # Minor pacing buffer for frame stability

        # CRITICAL REFACTORED ELEMENT: Force a focus blur by dispatching a TAB event
        element.send_keys(Keys.TAB)
        time.sleep(0.3)  # Give the frontend form state machine time to capture inputs

    def fill_traveller_info(self, full_name, dob, gender_string):
        """Injects source dataset profile passenger info block, translating explicit wait metrics."""
        self.logger.info(f"Populating name field container: {full_name}")
        self._safe_clear_and_type(TravellerPageLocators.FULL_NAME_INPUT, full_name)

        self.logger.info(f"Processing and passing raw date of birth data: {dob}")
        if dob:
            dob_field = WaitUtils.wait_for_element_visible(self.driver, TravellerPageLocators.DOB_INPUT)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dob_field)
            self.driver.execute_script("arguments[0].click();", dob_field)

            clean_dob_digits = str(dob).replace("-", "").strip()
            dob_field.send_keys(clean_dob_digits)

        self.logger.info(f"Locating gender selector component for profile value: {gender_string}")
        try:
            gender_normalized = str(gender_string).strip().capitalize()
            gender_radio_locator = TravellerPageLocators.get_dynamic_gender_radio(gender_normalized)

            gender_radio_element = WaitUtils.wait_for_presence_of_element(self.driver, gender_radio_locator)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", gender_radio_element)
            self.driver.execute_script("arguments[0].click();", gender_radio_element)
            self.logger.info(f"Successfully selected gender option: {gender_normalized}")
        except Exception as e:
            self.logger.error(f"Failed to interact with custom Gender option selection block: {str(e)}")

    def fill_contact_info(self, mobile_number, email_address):
        """Populates backend contact channels without experiencing element click interceptions."""
        self.logger.info(f"Processing communication node tracking configurations -> Ph: {mobile_number}")
        self._safe_clear_and_type(TravellerPageLocators.MOBILE_INPUT, mobile_number)
        self._safe_clear_and_type(TravellerPageLocators.EMAIL_INPUT, email_address)

    def complete_booking_flow(self):
        """Secures execution compliance declarations and dispatches final payment checkout calls."""
        self.logger.info("Filing statement approval criteria profiles...")
        try:
            box1 = WaitUtils.wait_for_presence_of_element(self.driver, TravellerPageLocators.COMPLIANCE_CHECKBOX_1)
            self.driver.execute_script("arguments[0].click();", box1)
        except Exception:
            pass

        try:
            box2 = WaitUtils.wait_for_presence_of_element(self.driver, TravellerPageLocators.COMPLIANCE_CHECKBOX_2)
            self.driver.execute_script("arguments[0].click();", box2)
        except Exception:
            pass

        self.logger.info("Executing final checkout submit sequence layout pass...")
        buy_btn = WaitUtils.wait_for_element_clickable(self.driver, TravellerPageLocators.FINAL_BUY_BTN)
        self.driver.execute_script("arguments[0].click();", buy_btn)

    def get_dob_error_message(self):
        """Helper method to scrape the DOB validation message natively using centralized sync loops."""
        element = WaitUtils.wait_for_element_visible(self.driver, TravellerPageLocators.DOB_ERROR_SPAN)
        return element.text

    def get_mobile_error_message(self):
        """Helper method to scrape the Mobile validation message natively using centralized sync loops."""
        element = WaitUtils.wait_for_element_visible(self.driver, TravellerPageLocators.MOBILE_ERROR_SPAN)
        return element.text

    def has_validation_errors(self):
        """Checks the page for any generic active validation error labels."""
        return len(self.driver.find_elements(*TravellerPageLocators.DOB_ERROR_SPAN_GENERIC)) > 0