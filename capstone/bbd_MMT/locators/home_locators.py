from selenium.webdriver.common.by import By

class HomePageLocators:
    CLOSE_LOGIN_MODAL = (By.CSS_SELECTOR, "span[data-cy='closeModal']")
    TRAVEL_INSURANCE_TAB = (By.CSS_SELECTOR, "li[data-cy='menu_TravelInsurance']")