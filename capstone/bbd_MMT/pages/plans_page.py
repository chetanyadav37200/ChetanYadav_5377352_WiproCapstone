# pages/plans_page.py

from pages.base_page import BasePage
from locators.plans_locators import PlansPageLocators


class PlansPage(BasePage):

    def is_choose_plan_present(self):
        self.logger.info("Checking if Choose Your Plan layout has rendered...")
        return self.is_displayed(PlansPageLocators.CHOOSE_PLAN_HEADER)

    def click_buy_now(self, plan_index=1):
        """Clicks the 'BUY NOW' button of a targeted plan column index card."""
        try:
            idx = int(str(plan_index).strip())
            if idx not in [1, 2, 3, 4]:
                idx = 1
        except Exception:
            idx = 1

        self.logger.info(f"Selecting insurance plan column position index card: [{idx}] via dynamic locators...")

        # Generating the targeted component xpath cleanly via the structural locator function
        dynamic_buy_now_btn = PlansPageLocators.get_dynamic_buy_now_btn(idx)
        self.click(dynamic_buy_now_btn)