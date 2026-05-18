import pytest
import time
from utils.csv_reader import CSVReader
from utils.screenshot_util import ScreenshotUtil
from utils.logger import LogGen
from utils.config_reader import ConfigReader
from pages.home_page import HomePage
from pages.insurance_page import InsurancePage
from pages.plans_page import PlansPage
from pages.traveller_page import TravellerPage
from pages.login_popup_page import LoginPopupPage

logger = LogGen.loggen()


def test_make_my_trip_insurance_e2e_single_flow(driver):
    home_page = HomePage(driver)
    insurance_page = InsurancePage(driver)
    plans_page = PlansPage(driver)
    traveller_page = TravellerPage(driver)
    login_popup = LoginPopupPage(driver)

    base_url = ConfigReader.get("base_url").strip()
    config_mobile = ConfigReader.get("mobile_number").strip()

    dataset = CSVReader.read_csv("insurance_data.csv")
    logger.info(f"Loaded {len(dataset)} records. Executing single-flow execution batch...")

    for index, data_row in enumerate(dataset):
        logger.info(f"--- Starting Flow Iteration {index + 1}: {data_row['name']} ---")

        try:
            if index > 0:
                logger.info(f"Resetting browser flow back to homepage: {base_url}")
                driver.get(base_url)

            # Step 1: Manage modals and initial navigations
            if index == 0:
                login_popup.close_popup_if_present()
            else:
                home_page.dismiss_login_if_present()

            home_page.click_travel_insurance()

            # Step 2: Form navigation validation hub
            assert insurance_page.is_insurance_page_open(), f"[{data_row['name']}] Error: Not on Insurance page layout!"
            insurance_page.click_explore_plans()

            # Step 3: Plans table validation grid
            assert plans_page.is_choose_plan_present(), f"[{data_row['name']}] Error: Plans matrix grid failed to load!"
            plans_page.click_buy_now()

            # Step 4: Populate user forms
            assert traveller_page.is_traveller_page_open(), f"[{data_row['name']}] Error: Checkout input profile screen missing!"
            traveller_page.fill_traveller_info(data_row['name'], data_row['dob'], data_row['gender'])
            traveller_page.fill_contact_info(data_row['mobile'], data_row['email'])

            # Step 5: Execute form submit and intercept authentication popups
            traveller_page.complete_booking_flow()
            time.sleep(2.5)

            # Step 6: Handle intercept popup, check consent, click Continue, and halt
            if login_popup.is_login_popup_displayed():
                login_popup.login_with_mobile_and_wait_for_otp(config_mobile)

            logger.info(
                f"--- Completed Flow Iteration {index + 1} Success: Form submitted and Continue button targeted ---")

            # === THE FIX: Stop the test execution right here cleanly ===
            logger.info("Single-flow target successfully achieved. Stopping automation run here.")
            break
            # ==========================================================

        except (AssertionError, Exception) as e:
            logger.error(f"Flow interrupted during profile process sequence [{data_row['name']}]: {str(e)}")
            ScreenshotUtil.capture_screenshot(driver, f"FlowError_{data_row['name'].replace(' ', '_')}")
            raise e