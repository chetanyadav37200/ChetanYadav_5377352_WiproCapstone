from selenium.webdriver.common.by import By


class TravellerPageLocators:
    TRAVELLER_PAGE_CHECKMARK = (By.XPATH,
                                "//*[contains(@data-test-id, 'H5Tag')] | //h5[contains(., 'Traveller Details')] | //div[contains(text(), 'Traveller Details')]")
    FULL_NAME_INPUT = (By.XPATH,
                       "//input[@id='FULL NAME'] | //input[@placeholder='Full Name'] | //input[contains(@placeholder, 'Name')]")
    DOB_INPUT = (By.XPATH, "//input[@id='DATE OF BIRTH'] | //input[@type='date']")
    MOBILE_INPUT = (By.XPATH,
                    "//input[@id='Mobile No.'] | //input[@type='tel'] | //input[contains(@placeholder, 'Mobile')]")
    EMAIL_INPUT = (By.XPATH,
                   "//input[@id='Email ID'] | //input[@type='email'] | //input[contains(@placeholder, 'Email')]")
    COMPLIANCE_CHECKBOX_1 = (By.XPATH,
                             "//input[@type='checkbox']/ancestor::label[1] | //span[contains(., 'Indian residents')]")
    COMPLIANCE_CHECKBOX_2 = (By.XPATH,
                             "//input[@type='checkbox']/ancestor::label[2] | //span[contains(., 'good health')]")
    FINAL_BUY_BTN = (By.XPATH,
                     "//button[contains(@class, 'LandingButtonStyle')] | //button[descendant::span[contains(text(), 'BUY FOR')]]")

    # Error Message Capture Nodes
    DOB_ERROR_SPAN = (By.XPATH, "//span[contains(text(), 'Date of Birth') or contains(text(), 'birth')]")
    MOBILE_ERROR_SPAN = (By.XPATH, "//span[@data-test-id='CountryCodeInput-ErrorTxt']")
    DOB_ERROR_SPAN_GENERIC = (By.XPATH,
                              "//span[@data-test-id='CountryCodeInput-ErrorTxt'] | //span[contains(text(), 'Birth')]")

    @staticmethod
    def get_dynamic_gender_radio(gender_normalized):
        """Generates dynamic xpath to grab accurate gender buttons contextually."""
        return (By.XPATH,
                f"//div[contains(@data-test-id, 'GenderTypeItem')]//div[contains(@class, 'RadioButtonStyle') and .//label[contains(text(), '{gender_normalized}')]] | //label[contains(text(), '{gender_normalized}')]/preceding-sibling::input[@type='radio'] | //div[contains(@class, 'RadioButtonStyle') and contains(., '{gender_normalized}')]")