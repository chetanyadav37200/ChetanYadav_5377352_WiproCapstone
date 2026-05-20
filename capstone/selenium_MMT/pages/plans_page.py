from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class PlansPage(BasePage):
    CHOOSE_PLAN_HEADER = (By.CSS_SELECTOR, "div[data-test-id='Header-HeaderWrapper']")

    FIRST_PLAN_CARD = (By.CSS_SELECTOR, "div[data-test-id='Card-CardWrapper']")

    # Keeping your original static locator here as a fallback baseline reference
    BUY_NOW_BTN = (By.XPATH,
                   "//div[@data-test-id='Card-CardWrapper'][1]//button[descendant-or-self::*[normalize-space(text())='BUY NOW']]")

    def is_choose_plan_present(self):
        self.logger.info("Checking if Choose Your Plan layout has rendered...")
        return self.is_displayed(self.CHOOSE_PLAN_HEADER)

    def click_buy_now(self, plan_index=1):
        """
        Clicks the 'BUY NOW' button of a targeted plan column index (1, 2, 3, or 4).
        Defaults to your original choice [1] if no index is passed.
        """
        # Validate that incoming indices from your CSV rows are handled safely
        try:
            idx = int(str(plan_index).strip())
            if idx not in [1, 2, 3, 4]:
                idx = 1
        except Exception:
            idx = 1

        self.logger.info(f"Selecting insurance plan column position index card: [{idx}] via 'BUY NOW' hook...")

        # Dynamically inject the column index into your exact XPath structure
        dynamic_buy_now_btn = (By.XPATH, f"//div[@data-test-id='Card-CardWrapper'][{idx}]//button[descendant-or-self::*[normalize-space(text())='BUY NOW']]")

        # Execute click using your framework's native self.click() wrapper method
        self.click(dynamic_buy_now_btn)