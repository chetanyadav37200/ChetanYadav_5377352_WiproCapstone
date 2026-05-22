from selenium.webdriver.common.by import By

class InsurancePageLocators:
    INSURANCE_PAGE_CHECKMARK = (By.XPATH, "//h1[contains(., 'International Travel + Medical Insurance')] | //h1[.//span[contains(text(), 'International Travel')]]")
    EXPLORE_PLANS_BTN = (By.XPATH, "//button[contains(translate(., 'explore plans', 'EXPLORE PLANS'), 'EXPLORE PLANS')] | //button[normalize-space()='EXPLORE PLANS']")
    COUNTRY_DROPDOWN_CONTAINER = (By.XPATH, "//p[contains(normalize-space(text()), 'COUNTRY/REGION')]/ancestor::div[1] | //div[p[contains(normalize-space(text()), 'COUNTRY/REGION')]] | //div[contains(@class, 'khlxBq')]")
    SEARCH_COUNTRY_INPUT = (By.XPATH, "//input[@placeholder='Search Country/Region']")
    DROPDOWN_POPUP_PANEL = (By.XPATH, "//input[@placeholder='Search Country/Region']")
    APPLY_COUNTRY_BTN = (By.XPATH, "//span[text()='Apply']/ancestor::button | //button[contains(., 'Apply')] | //span[text()='Apply']")
    TRAVELLERS_DROPDOWN_TRIGGER = (By.XPATH, "//p[contains(text(), 'No. of Travellers')]/ancestor::div[1] | //div[p[contains(text(), 'No. of Travellers')]]")