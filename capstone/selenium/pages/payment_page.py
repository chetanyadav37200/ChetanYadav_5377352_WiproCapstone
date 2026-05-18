import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class PaymentPage(BasePage):
    # --- Identification Locators ---
    PAYMENT_OPTIONS_HEADER = (By.CSS_SELECTOR, "[data-test-id='paymode-list-wrap']")

    # --- Payment Mode Selections ---
    CREDIT_DEBIT_CARD_TAB = (By.XPATH,
                             "//div[@data-test-id='paymode-inner-container' and contains(., 'Credit & Debit Cards')]")

    # --- Card Input Fields ---
    CARD_NUMBER_INPUT = (By.CSS_SELECTOR, "[data-test-id='card-fields-number-row'] input")
    EXPIRY_MONTH_DROPDOWN = (By.CSS_SELECTOR, "[data-test-id='card-fields-expiry-month-select-container']")
    EXPIRY_YEAR_DROPDOWN = (By.CSS_SELECTOR, "[data-test-id='card-fields-expiry-year-select-container']")
    CVV_INPUT = (By.CSS_SELECTOR, "[data-test-id='card-fields-cvv-container'] input")

    def is_payment_page_open(self):
        """Validates if the browser has successfully rendered the MakeMyTrip payment hub."""
        self.logger.info("Verifying if Payment options gateway view is open...")
        return self.is_displayed(self.PAYMENT_OPTIONS_HEADER)

    def select_credit_debit_card(self):
        """Navigates to the card entry form layout using a safe JavaScript execution fallback."""
        self.logger.info("Selecting Credit & Debit Cards option...")
        card_tab = self.driver.find_element(*self.CREDIT_DEBIT_CARD_TAB)
        self.driver.execute_script("arguments[0].click();", card_tab)

    def select_dropdown_value(self, container_locator, value):
        """Helper method to handle custom web component select dropdown containers."""
        self.click(container_locator)
        time.sleep(0.5)

        option_locator = (By.XPATH,
                          f"//div[contains(@class, 'dropdown')]//*[normalize-space(text())='{value}'] | //*[text()='{value}']")
        self.click(option_locator)

    def fill_card_details(self, card_num, exp_month, exp_year, cvv):
        """Fills out the secured payment form using explicit parameters."""
        self.logger.info("Entering credit card credentials...")
        self.enter_text(self.CARD_NUMBER_INPUT, card_num)

        # Handle the dynamic custom dropdown menus for MM / YY selectors
        self.select_dropdown_value(self.EXPIRY_MONTH_DROPDOWN, exp_month)
        self.select_dropdown_value(self.EXPIRY_YEAR_DROPDOWN, exp_year)

        self.enter_text(self.CVV_INPUT, cvv)