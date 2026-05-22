from selenium.webdriver.common.by import By

class LoginPopupLocators:
    MOBILE_INPUT = (By.CSS_SELECTOR, "input[data-cy='userName']")
    CONTINUE_BTN = (By.CSS_SELECTOR, "button[data-cy='continueBtn']")
    CLOSE_MODAL_BTN = (By.CSS_SELECTOR, "span[data-cy='closeModal']")
    CONSENT_CHECKBOX = (By.CSS_SELECTOR, "input[data-cy='user-consent-checkbox']")