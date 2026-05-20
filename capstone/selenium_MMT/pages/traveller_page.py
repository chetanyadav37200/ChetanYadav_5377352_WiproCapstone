import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class TravellerPage(BasePage):
    # --- Traveler Profile Initialization Locators ---
    TRAVELLER_PAGE_CHECKMARK = (By.XPATH, "//*[contains(@data-test-id, 'H5Tag')] | //h5[contains(., 'Traveller Details')] | //div[contains(text(), 'Traveller Details')]")

    # --- Unified Passenger Input Fields ---
    FULL_NAME_INPUT = (By.XPATH, "//input[@id='FULL NAME'] | //input[@placeholder='Full Name'] | //input[contains(@placeholder, 'Name')]")
    DOB_INPUT = (By.XPATH, "//input[@id='DATE OF BIRTH'] | //input[@type='date']")

    # --- Dynamic Contact Fields ---
    MOBILE_INPUT = (By.XPATH, "//input[@id='Mobile No.'] | //input[@type='tel'] | //input[contains(@placeholder, 'Mobile')]")
    EMAIL_INPUT = (By.XPATH, "//input[@id='Email ID'] | //input[@type='email'] | //input[contains(@placeholder, 'Email')]")

    # --- Submission Constraints ---
    COMPLIANCE_CHECKBOX_1 = (By.XPATH, "//input[@type='checkbox']/ancestor::label[1] | //span[contains(., 'Indian residents')]")
    COMPLIANCE_CHECKBOX_2 = (By.XPATH, "//input[@type='checkbox']/ancestor::label[2] | //span[contains(., 'good health')]")
    FINAL_BUY_BTN = (By.XPATH, "//button[contains(@class, 'LandingButtonStyle')] | //button[descendant::span[contains(text(), 'BUY FOR')]]")

    # --- Refactored Validation Error Locators ---
    DOB_ERROR_SPAN = (By.XPATH, "//span[contains(text(), 'Date of Birth') or contains(text(), 'birth')]")
    MOBILE_ERROR_SPAN = (By.XPATH, "//span[@data-test-id='CountryCodeInput-ErrorTxt']")
    DOB_ERROR_SPAN_GENERIC = (By.XPATH, "//span[@data-test-id='CountryCodeInput-ErrorTxt'] | //span[contains(text(), 'Birth')]")

    def is_traveller_page_open(self):
        """Dynamically waits for the checkout traveler screen to finish initializing."""
        self.logger.info("Waiting explicitly for checkout form containers to mount...")
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.TRAVELLER_PAGE_CHECKMARK))
            return element.is_displayed()
        except Exception:
            return False

    def is_traveller_header_present(self):
        """Validates if the header block layout component is cleanly rendered on screen."""
        try:
            element = self.wait.until(EC.presence_of_element_located(self.TRAVELLER_PAGE_CHECKMARK))
            return element.is_displayed()
        except Exception:
            return False

    def _safe_clear_and_type(self, locator, text_value):
        """
        Ensures input fields accurately register data inside single-page React environments.
        Bypasses layout intercepts, cleans the target, and keys inside text fragments natively.
        """
        element = self.wait.until(EC.visibility_of_element_located(locator))

        # Center target element on screen to drop focus cleanly
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.driver.execute_script("arguments[0].click();", element)

        # Clear fields natively via structural keyboard emulations
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACKSPACE)

        # Type value character-by-character to guarantee state binding registration
        for char in str(text_value):
            element.send_keys(char)

    def fill_traveller_info(self, full_name, dob, gender_string):
        """Injects your source dataset profile passenger info block, translating dates and selecting radio choices."""
        self.logger.info(f"Populating name field container: {full_name}")
        self._safe_clear_and_type(self.FULL_NAME_INPUT, full_name)

        self.logger.info(f"Processing and passing raw date of birth data: {dob}")
        if dob:
            dob_field = self.wait.until(EC.visibility_of_element_located(self.DOB_INPUT))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dob_field)
            self.driver.execute_script("arguments[0].click();", dob_field)

            clean_dob_digits = str(dob).replace("-", "").strip()
            dob_field.send_keys(clean_dob_digits)

        self.logger.info(f"Locating gender selector component for profile value: {gender_string}")
        try:
            gender_normalized = str(gender_string).strip().capitalize()
            gender_xpath = f"//div[contains(@data-test-id, 'GenderTypeItem')]//div[contains(@class, 'RadioButtonStyle') and .//label[contains(text(), '{gender_normalized}')]] | //label[contains(text(), '{gender_normalized}')]/preceding-sibling::input[@type='radio'] | //div[contains(@class, 'RadioButtonStyle') and contains(., '{gender_normalized}')]"

            gender_radio_element = self.wait.until(EC.presence_of_element_located((By.XPATH, gender_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", gender_radio_element)
            self.driver.execute_script("arguments[0].click();", gender_radio_element)
            self.logger.info(f"Successfully selected gender option: {gender_normalized}")
        except Exception as e:
            self.logger.error(f"Failed to resolve or interact with custom Gender option selection block: {str(e)}")

    def fill_contact_info(self, mobile_number, email_address):
        """Populates backend contact channels without experiencing element click interceptions."""
        self.logger.info(f"Processing communication node tracking configurations -> Ph: {mobile_number}")
        self._safe_clear_and_type(self.MOBILE_INPUT, mobile_number)
        self._safe_clear_and_type(self.EMAIL_INPUT, email_address)

    def complete_booking_flow(self):
        """Secures execution compliance declarations and dispatches final payment checkout calls."""
        self.logger.info("Filing statement approval criteria profiles...")
        try:
            box1 = self.wait.until(EC.presence_of_element_located(self.COMPLIANCE_CHECKBOX_1))
            self.driver.execute_script("arguments[0].click();", box1)
        except Exception:
            pass

        try:
            box2 = self.wait.until(EC.presence_of_element_located(self.COMPLIANCE_CHECKBOX_2))
            self.driver.execute_script("arguments[0].click();", box2)
        except Exception:
            pass

        self.logger.info("Executing final checkout submit sequence layout pass...")
        buy_btn = self.wait.until(EC.element_to_be_clickable(self.FINAL_BUY_BTN))
        self.driver.execute_script("arguments[0].click();", buy_btn)

    # --- Refactored Validation Error Methods ---
    def get_dob_error_message(self):
        """Helper method to scrape the DOB validation message natively from the page object."""
        element = self.wait.until(EC.visibility_of_element_located(self.DOB_ERROR_SPAN))
        return element.text

    def get_mobile_error_message(self):
        """Helper method to scrape the Mobile validation message natively from the page object."""
        element = self.wait.until(EC.visibility_of_element_located(self.MOBILE_ERROR_SPAN))
        return element.text

    def has_validation_errors(self):
        """Checks the page for any generic active validation error labels."""
        return len(self.driver.find_elements(*self.DOB_ERROR_SPAN_GENERIC)) > 0