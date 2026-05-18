from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class TravellerPage(BasePage):
    TRAVELLER_PAGE_HEADER = (By.CSS_SELECTOR, "h5[data-test-id='H5Tag-H5TagStyle']")

    NAME_INPUT = (By.XPATH,
                  "//div[@data-test-id='LandingInput-InputWrap' and .//label[contains(., 'FULL NAME')]]//input")
    DOB_INPUT = (By.XPATH,
                 "//div[@data-test-id='LandingInput-InputWrap' and .//label[contains(., 'DATE OF BIRTH')]]//input")

    # Selects gender radio container components reliably via structural text
    # --- Updated Locators inside TravellerPage class ---

    # Target the inner structural components containing the explicit literal text labels
    GENDER_MALE = (By.XPATH,
                   "//div[@data-test-id='ExpandedForm-FormFields-GenderTypeItem']//*[normalize-space(text())='Male'] | //span[normalize-space(text())='Male']")
    GENDER_FEMALE = (By.XPATH,
                     "//div[@data-test-id='ExpandedForm-FormFields-GenderTypeItem']//*[normalize-space(text())='Female'] | //span[normalize-space(text())='Female']")

    # --- Contact Details Section ---
    # Targets input forms explicitly by using the precise text ID bindings shown in DOM
    MOBILE_INPUT = (By.CSS_SELECTOR, "input[id='Mobile No.']")
    EMAIL_INPUT = (By.XPATH,
                   "//div[@data-test-id='LandingInput-InputWrap' and .//label[contains(., 'Email ID')]]//input")

    # --- Declarations & Final Submission ---
    # Locates standard interactive checkbox components via their parent wrappers
    TERMS_CHECKBOX_1 = (By.XPATH,
                        "(//div[@data-test-id='TravellerCommonComp-ConfirmTnc'])[1]//input[@type='checkbox'] | (//div[@data-test-id='TravellerCommonComp-ConfirmTnc'])[1]")
    TERMS_CHECKBOX_2 = (By.XPATH,
                        "(//div[@data-test-id='TravellerCommonComp-ConfirmTnc'])[2]//input[@type='checkbox'] | (//div[@data-test-id='TravellerCommonComp-ConfirmTnc'])[2]")

    # Fixed syntax string structure to find final pricing submit button
    BUY_FOR_BTN = (By.CSS_SELECTOR, "button[data-test-id='LandingButton-LandingButtonStyle']")

    def is_traveller_page_open(self):
        """Checks if the checkout layout page has rendered."""
        self.logger.info("Verifying if checkout traveler details page is fully displayed...")
        return self.is_displayed(self.TRAVELLER_PAGE_HEADER)

    def fill_traveller_info(self, name, dob, gender):
        """Enters required traveler credentials."""
        self.logger.info(f"Filling credentials data for traveller: {name} ({gender})")
        self.enter_text(self.NAME_INPUT, name)
        self.enter_text(self.DOB_INPUT, dob)
        if gender.lower() == 'male':
            self.click(self.GENDER_MALE)
        else:
            self.click(self.GENDER_FEMALE)

    def fill_contact_info(self, mobile, email):
        """Fills contact details."""
        self.logger.info(f"Filling primary communication route data -> Ph: {mobile} | Email: {email}")
        self.enter_text(self.MOBILE_INPUT, mobile)
        self.enter_text(self.EMAIL_INPUT, email)

    def complete_booking_flow(self):
        """Accepts conditional requirements and proceeds directly to payment gateways."""
        self.logger.info("Accepting compliance declarations and committing checkout submission...")

        # 1. Resolve elements
        cb1 = self.driver.find_element(*self.TERMS_CHECKBOX_1)
        cb2 = self.driver.find_element(*self.TERMS_CHECKBOX_2)
        submit_btn = self.driver.find_element(*self.BUY_FOR_BTN)

        # 2. Scroll elements into view
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cb1)

        # 3. Use JavaScript clicks to safely toggle checkboxes
        try:
            cb1.click()
        except Exception:
            self.logger.warning("Standard click intercepted on Checkbox 1. Bypassing via JS Click...")
            self.driver.execute_script("arguments[0].click();", cb1)

        try:
            cb2.click()
        except Exception:
            self.logger.warning("Standard click intercepted on Checkbox 2. Bypassing via JS Click...")
            self.driver.execute_script("arguments[0].click();", cb2)

        # 4. Final Click onto the Buy/Submit Button via JS to bypass floating footer interceptors
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
        try:
            submit_btn.click()
        except Exception:
            self.logger.warning("Standard click intercepted on Buy Button. Bypassing via JS Click...")
            self.driver.execute_script("arguments[0].click();", submit_btn)