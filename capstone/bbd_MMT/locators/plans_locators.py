from selenium.webdriver.common.by import By

class PlansPageLocators:
    CHOOSE_PLAN_HEADER = (By.CSS_SELECTOR, "div[data-test-id='Header-HeaderWrapper']")
    FIRST_PLAN_CARD = (By.CSS_SELECTOR, "div[data-test-id='Card-CardWrapper']")
    BUY_NOW_BTN = (By.XPATH, "//div[@data-test-id='Card-CardWrapper'][1]//button[descendant-or-self::*[normalize-space(text())='BUY NOW']]")

    @staticmethod
    def get_dynamic_buy_now_btn(plan_index):
        """Generates an explicit column targeted locator dynamically."""
        return (By.XPATH, f"//div[@data-test-id='Card-CardWrapper'][{plan_index}]//button[descendant-or-self::*[normalize-space(text())='BUY NOW']]")