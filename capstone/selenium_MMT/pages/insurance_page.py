import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.screenshot_util import ScreenshotUtil  # Imported Utility


class InsurancePage(BasePage):
    # --- Locators ---
    INSURANCE_PAGE_CHECKMARK = (By.XPATH,
                                "//h1[contains(., 'International Travel + Medical Insurance')] | //h1[.//span[contains(text(), 'International Travel')]]")
    EXPLORE_PLANS_BTN = (By.XPATH,
                         "//button[contains(translate(., 'explore plans', 'EXPLORE PLANS'), 'EXPLORE PLANS')] | //button[normalize-space()='EXPLORE PLANS']")
    COUNTRY_DROPDOWN_CONTAINER = (By.XPATH,
                                  "//p[contains(normalize-space(text()), 'COUNTRY/REGION')]/ancestor::div[1] | //div[p[contains(normalize-space(text()), 'COUNTRY/REGION')]] | //div[contains(@class, 'khlxBq')]")
    SEARCH_COUNTRY_INPUT = (By.XPATH, "//input[@placeholder='Search Country/Region']")
    DROPDOWN_POPUP_PANEL = (By.XPATH, "//input[@placeholder='Search Country/Region']")
    APPLY_COUNTRY_BTN = (By.XPATH,
                         "//span[text()='Apply']/ancestor::button | //button[contains(., 'Apply')] | //span[text()='Apply']")
    TRAVELLERS_DROPDOWN_TRIGGER = (By.XPATH,
                                   "//p[contains(text(), 'No. of Travellers')]/ancestor::div[1] | //div[p[contains(text(), 'No. of Travellers')]]")

    def is_insurance_page_open(self):
        """Validates that the insurance main dashboard context has rendered successfully."""
        return self.is_displayed(self.INSURANCE_PAGE_CHECKMARK)

    def select_country(self, country_name):
        """Opens dropdown container, clears pre-selected options, searches custom inputs, and applies."""
        self.logger.info("Opening Country/Region selection dropdown popup...")
        container = self.wait.until(EC.presence_of_element_located(self.COUNTRY_DROPDOWN_CONTAINER))
        self.driver.execute_script("arguments[0].click();", container)
        self.wait.until(EC.visibility_of_element_located(self.DROPDOWN_POPUP_PANEL))

        self.logger.info("Targeting and removing default 'Thailand' selection...")
        try:
            thailand_element = self.driver.find_element(By.XPATH,
                                                        "//li[contains(., 'Thailand')]//span | //li[contains(., 'Thailand')]")
            self.driver.execute_script("arguments[0].click();", thailand_element)
            self.logger.info("Default selection cleared.")
            time.sleep(0.5)
        except Exception as e:
            self.logger.warning(f"Deselection step skipped or already clear: {str(e)}")

        if not country_name or country_name.strip() == "":
            self.logger.info("Blank country input detected in CSV row. Saving empty form layout...")
            apply_btn = self.wait.until(EC.visibility_of_element_located(self.APPLY_COUNTRY_BTN))
            self.driver.execute_script("arguments[0].click();", apply_btn)
            return

        self.logger.info(f"Injecting search phrase query: {country_name}")
        search_box = self.wait.until(EC.element_to_be_clickable(self.SEARCH_COUNTRY_INPUT))
        search_box.click()
        search_box.send_keys(Keys.CONTROL + "a")
        search_box.send_keys(Keys.BACKSPACE)

        for char in str(country_name):
            search_box.send_keys(char)
        time.sleep(0.5)

        self.logger.info(f"Checking filtered list match row for: {country_name}")
        target_row_xpath = f"//ul[contains(@class, 'db')]//li[contains(., '{country_name}')] | //span[normalize-space(text())='{country_name}']"
        target_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, target_row_xpath)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_element)
        self.driver.execute_script("arguments[0].click();", target_element)

        time.sleep(1.0)

        # ROUTED TO FOLDER: Captured state sent via utility instance
        scr_name = f"Country_Input_State_{country_name}"
        screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, scr_name)
        allure.attach.file(screenshot_path, name=scr_name, attachment_type=allure.attachment_type.PNG)

        self.logger.info("Committing choices via updated JavaScript 'APPLY' injection...")
        apply_btn_element = self.wait.until(EC.presence_of_element_located(self.APPLY_COUNTRY_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", apply_btn_element)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", apply_btn_element)

        try:
            self.wait.until(EC.invisibility_of_element_located(self.SEARCH_COUNTRY_INPUT))
            self.logger.info("Apply button clicked successfully and dropdown closed.")
        except Exception:
            self.logger.warning("Dropdown didn't close instantly, trying an alternate fallback click on Apply...")
            fallback_apply = self.driver.find_element(By.XPATH, "//span[text()='Apply']")
            self.driver.execute_script("arguments[0].click();", fallback_apply)
            time.sleep(1.0)

    def select_travellers_count(self, count_value):
        """Triggers traveler selection panel and sets double-digit values."""
        self.logger.info(f"Triggering traveler count selection pane for value: {count_value}")

        trigger_element = self.wait.until(EC.element_to_be_clickable(self.TRAVELLERS_DROPDOWN_TRIGGER))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trigger_element)
        self.driver.execute_script("arguments[0].click();", trigger_element)

        try:
            cleaned_number = int(str(count_value).strip())
            formatted_count = f"{cleaned_number:02d}"
        except Exception:
            formatted_count = "01"

        self.logger.info(f"Targeting formatted DOM text row option: {formatted_count}")

        target_option_xpath = (
            f"//div[contains(@class, 'hLrkT') or contains(@class, 'clickT')]//div[text()='{formatted_count}'] | "
            f"//div[text()='{formatted_count}' and contains(@style, 'cursor')] | "
            f"//div[contains(text(), '{formatted_count}') and not(contains(@class, 'No'))]"
        )

        option_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, target_option_xpath)))
        time.sleep(0.5)

        # ROUTED TO FOLDER: Mid-test checkpoint captured safely
        scr_name = f"Travellers_Dropdown_Before_Click_{formatted_count}"
        screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, scr_name)
        allure.attach.file(screenshot_path, name=scr_name, attachment_type=allure.attachment_type.PNG)

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option_element)
        self.driver.execute_script("arguments[0].click();", option_element)
        self.logger.info(f"Successfully selected traveler option: {formatted_count}")
        time.sleep(0.5)

    def click_explore_plans(self):
        """Force clicks the final search activation button via JavaScript bypass."""
        self.logger.info("Clicking EXPLORE PLANS button to trigger matrix generation...")
        explore_btn = self.wait.until(EC.presence_of_element_located(self.EXPLORE_PLANS_BTN))

        # ROUTED TO FOLDER: final layout view check
        scr_name = "Landing_Page_Before_Explore_Click"
        screenshot_path = ScreenshotUtil.capture_screenshot(self.driver, scr_name)
        allure.attach.file(screenshot_path, name=scr_name, attachment_type=allure.attachment_type.PNG)

        self.driver.execute_script("arguments[0].click();", explore_btn)