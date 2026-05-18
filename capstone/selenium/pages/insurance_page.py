import csv
import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InsurancePage(BasePage):
    # --- Form & Navigation Locators ---
    INSURANCE_PAGE_CHECKMARK = (By.XPATH, "//h1[contains(., 'International Travel + Medical Insurance')]")
    EXPLORE_PLANS_BTN = (By.XPATH, "//button[descendant-or-self::*[normalize-space(text())='EXPLORE PLANS']]")

    # --- Input Field Containers ---
    COUNTRY_DROPDOWN_CONTAINER = (By.XPATH,
                                  "//div[p[contains(normalize-space(text()), 'COUNTRY/REGION')]] | //div[contains(normalize-space(text()), 'COUNTRY/REGION')]")
    START_DATE_TRIGGER = (By.XPATH, "//div[p[contains(normalize-space(text()), 'Start Date')]]")
    END_DATE_TRIGGER = (By.XPATH, "//div[p[contains(normalize-space(text()), 'End Date')]]")
    TRAVELLERS_TRIGGER = (By.XPATH, "//div[p[contains(normalize-space(text()), 'No. of Travellers')]]")

    # --- Modal Inside Components ---
    SEARCH_COUNTRY_INPUT = (By.XPATH, "//input[@placeholder='Search Country/Region']")
    APPLY_COUNTRY_BTN = (By.XPATH, "//button[normalize-space(text())='APPLY']")

    # Target any checked checkboxes inside the open country list view layer to clear previous defaults
    ACTIVE_CHECKED_COUNTRIES = (By.XPATH,
                                "//li[.//input[@type='checkbox' and @checked]] | //div[input[@type='checkbox' and @checked]]")

    def is_insurance_page_open(self):
        return self.is_displayed(self.INSURANCE_PAGE_CHECKMARK)

    def select_country(self, country_name):
        """
        Robust country selection workflow: Opens container, clears existing defaults,
        searches for the user's input country, clicks its checkbox, and applies.
        """
        # Step 1: Open the Country/Region dropdown container
        self.logger.info("Opening Country/Region selection dropdown...")
        self.click(self.COUNTRY_DROPDOWN_CONTAINER)
        time.sleep(1)  # Allow modal transition animation to complete safely

        # Step 2: Clear pre-selected countries (like Thailand) first
        self.logger.info("Checking for pre-selected countries to uncheck...")
        try:
            # Locate any checkboxes that are currently active/checked
            active_checkboxes = self.driver.find_elements(By.XPATH,
                                                          "//ul[@data-test-id='paymode-list-items']//input[@type='checkbox' and @checked] | //input[@type='checkbox' and @checked]/following-sibling::span | //li[contains(., 'Thailand')]//input[@type='checkbox']")
            for checkbox in active_checkboxes:
                # If the checkbox element itself is non-clickable due to custom styling, click its parent or label wrapper
                self.driver.execute_script("arguments[0].click();", checkbox)
                self.logger.info("Default country (Thailand) unchecked successfully.")
            time.sleep(0.5)
        except Exception as e:
            self.logger.warning(f"Could not uncheck default selections: {str(e)}")

        # If the user input from CSV is blank, stop here after clearing the form
        if not country_name or country_name.strip() == "":
            self.logger.info("No country provided in CSV. Leaving selection blank.")
            return

        # Step 3: Search for the new country given by the user (e.g., 'UAE')
        self.logger.info(f"Searching for user specified country: {country_name}")
        search_box = self.driver.find_element(*self.SEARCH_COUNTRY_INPUT)
        search_box.click()
        search_box.send_keys(Keys.CONTROL + "a")
        search_box.send_keys(Keys.DELETE)
        search_box.send_keys(country_name)
        time.sleep(1)  # Wait for the filtered list to update on screen

        # Step 4: Click the checkbox next to the searched country
        self.logger.info(f"Clicking the checkbox for: {country_name}")
        # This targets the specific row element checkbox container matching your searched string
        target_country_checkbox = (By.XPATH,
                                   f"//li[contains(., '{country_name}')]//input[@type='checkbox'] | //span[normalize-space(text())='{country_name}']/preceding-sibling::input[@type='checkbox'] | //li[contains(., '{country_name}')]")

        target_element = self.driver.find_element(*target_country_checkbox)
        self.driver.execute_script("arguments[0].click();", target_element)
        time.sleep(0.5)

        # Step 5: Click the 'APPLY' button to lock in the choice
        self.logger.info("Clicking on 'APPLY' button to finalize country selection...")
        if self.is_displayed(self.APPLY_COUNTRY_BTN):
            apply_button = self.driver.find_element(*self.APPLY_COUNTRY_BTN)
            self.driver.execute_script("arguments[0].click();", apply_button)
        time.sleep(1)

    def select_dates(self, start_day, start_month, start_year, end_day, end_month, end_year):
        """Interacts with the dynamic calendar UI views to map target flight schedules."""
        # --- Handle Start Date ---
        self.logger.info(f"Setting Start Date to: {start_day} {start_month} '{start_year}")
        self.click(self.START_DATE_TRIGGER)
        time.sleep(0.5)

        # Scopes choice selection directly under the targeted Month container layout view grid element
        start_day_locator = (By.XPATH,
                             f"//div[contains(normalize-space(.), '{start_month}') and contains(normalize-space(.), '{start_year}')]//p[normalize-space(text())='{start_day}'] | //div[p[text()='{start_day}']]")
        self.click(start_day_locator)
        time.sleep(0.5)

        # --- Handle End Date ---
        self.logger.info(f"Setting End Date to: {end_day} {end_month} '{end_year}")
        self.click(self.END_DATE_TRIGGER)
        time.sleep(0.5)

        end_day_locator = (By.XPATH,
                           f"//div[contains(normalize-space(.), '{end_month}') and contains(normalize-space(.), '{end_year}')]//p[normalize-space(text())='{end_day}'] | //div[p[text()='{end_day}']]")
        self.click(end_day_locator)
        time.sleep(0.5)

    def select_travellers(self, count):
        """Sets the precise row count inside the dropdown layout panel viewport."""
        self.logger.info(f"Setting number of travellers to: {count}")
        self.click(self.TRAVELLERS_TRIGGER)
        time.sleep(0.5)

        # Pad number string sequence matching data layouts formats (e.g., '1' -> '01')
        formatted_count = str(count).zfill(2)

        traveller_option = (By.XPATH,
                            f"//li[normalize-space(text())='{formatted_count}'] | //p[normalize-space(text())='{formatted_count}'] | //span[normalize-space(text())='{formatted_count}']")
        self.click(traveller_option)
        time.sleep(0.5)

    def click_explore_plans(self):
        self.click(self.EXPLORE_PLANS_BTN)

    def run_search_from_csv(self, csv_file_path):
        """Parses rows sequentially tracking parameter variables data maps inputs."""
        self.logger.info(f"Loading complete search parameters from dataset source path: {csv_file_path}")
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                country = row['Country']
                travellers = row['Travellers']

                s_day = row['StartDay']
                s_month = row['StartMonth']
                s_year = row['StartYear']

                e_day = row['EndDay']
                e_month = row['EndMonth']
                e_year = row['EndYear']

                self.select_country(country)

                # Only execute date picking and traveller mappings if a country was intentionally selected
                if country and country.strip() != "":
                    self.select_dates(s_day, s_month, s_year, e_day, e_month, e_year)
                    self.select_travellers(travellers)
                    self.click_explore_plans()
                break