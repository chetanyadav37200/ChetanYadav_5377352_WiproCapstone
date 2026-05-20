import allure
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


@allure.feature("Travel Insurance Automation")
@allure.story("End-to-End Insurance Booking Flow with Dynamic Data")
def test_make_my_trip_insurance_e2e_single_flow(driver):
    home_page = HomePage(driver)
    insurance_page = InsurancePage(driver)
    plans_page = PlansPage(driver)
    traveller_page = TravellerPage(driver)
    login_popup = LoginPopupPage(driver)

    base_url = ConfigReader.get("base_url").strip()
    config_mobile = ConfigReader.get("mobile_number").strip()

    # Read data dynamically from your CSV file
    dataset = CSVReader.read_csv("insurance_data.csv")
    logger.info(f"Loaded {len(dataset)} records. Executing single-flow execution batch...")

    for index, data_row in enumerate(dataset):
        logger.info(f"--- Starting Flow Iteration {index + 1} for: {data_row.get('name', 'Profile Row')} ---")

        try:
            if index > 0:
                logger.info(f"Resetting browser flow back to homepage: {base_url}")
                driver.get(base_url)

            # ----------------------------------------------------------------
            # Step 1: Manage Modals and Navigation
            # ----------------------------------------------------------------
            with allure.step("Step 1: Dismiss login popup alerts and switch to Travel Insurance tab"):
                if index == 0:
                    login_popup.close_popup_if_present()
                else:
                    home_page.dismiss_login_if_present()

                home_page.click_travel_insurance()

                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="Step_1_Travel_Insurance_Landing_Page",
                    attachment_type=allure.attachment_type.PNG
                )

            # ----------------------------------------------------------------
            # Step 2: Form Configuration (Country Filtering & Travellers Count)
            # ----------------------------------------------------------------
            with allure.step("Step 2: Configure country destinations, traveler count, and submit search form"):
                assert insurance_page.is_insurance_page_open(), f"[{data_row.get('name')}] Error: Not on Insurance page layout!"

                # Normalize row dictionary keys to lowercase to avoid header mismatches
                row_data_clean = {k.lower().strip(): str(v).strip() for k, v in data_row.items()}

                target_country = row_data_clean.get('country', 'UAE')
                target_travellers = row_data_clean.get('travellers', '1')

                # 1. Inject destination country choice
                insurance_page.select_country(target_country)

                # 2. NEW INJECTION: Inject number of travelers dynamically from CSV row
                insurance_page.select_travellers_count(target_travellers)

                # Trigger search submission after fields match configuration mapping values
                logger.info("Directly triggering search submission via Explore Plans...")
                insurance_page.click_explore_plans()

                # CRITICAL ARCHITECTURAL BUFFER:
                # Gives the single-page application router time to freeze inputs and dispatch network requests
                time.sleep(2.5)

            # ----------------------------------------------------------------
            # Step 3: Plans Table Verification (Updated with index parsing)
            # ----------------------------------------------------------------
            with allure.step("Step 3: Validate available insurance matrices and click Buy Now"):
                assert plans_page.is_choose_plan_present(), f"[{data_row.get('name')}] Error: Plans matrix grid failed to load!"

                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="Step_3_Insurance_Plans_Grid_Visible",
                    attachment_type=allure.attachment_type.PNG
                )

                # Fetch target dynamic column entry selection from CSV dataset row maps
                # Defaults to 1 if the 'plan_index' header column is left completely blank
                target_plan_index = row_data_clean.get('plan_index', 1)
                plans_page.click_buy_now(target_plan_index)
                time.sleep(2.0)  # Safe landing gap to allow checkout session initialization to complete

            # ----------------------------------------------------------------
            # Step 4: Populate Checkout Forms
            # ----------------------------------------------------------------
            with allure.step("Step 4: Fill passenger identification metadata and communication endpoints"):
                assert traveller_page.is_traveller_page_open(), f"[{data_row.get('name')}] Error: Checkout input profile screen missing!"

                # Input traveler information
                traveller_page.fill_traveller_info(data_row['name'], data_row['dob'], data_row['gender'])

                # Input primary contact information
                traveller_page.fill_contact_info(data_row['mobile'], data_row['email'])

            # ----------------------------------------------------------------
            # Step 5: Execute Flow Submission
            # ----------------------------------------------------------------
            with allure.step("Step 5: Accept compliance terms declaration checkboxes and submit details"):
                traveller_page.complete_booking_flow()

            # ----------------------------------------------------------------
            # Step 6: Handle Authentication Intercepts
            # ----------------------------------------------------------------
            with allure.step("Step 6: Handle OTP login popup screen checks if visible"):
                if login_popup.is_login_popup_displayed():
                    allure.attach(
                        driver.get_screenshot_as_png(),
                        name="Step_6_Authentication_OTP_Prompt_Intercepted",
                        attachment_type=allure.attachment_type.PNG
                    )
                    login_popup.login_with_mobile_and_wait_for_otp(config_mobile)

            logger.info(f"--- Completed Flow Iteration {index + 1} Success ---")
            logger.info("Single-flow target successfully achieved. Stopping automation run here.")
            break

        except (AssertionError, Exception) as e:
            clean_name = data_row.get('name', 'Error').replace(' ', '_')
            logger.error(
                f"Flow interrupted during profile process sequence [{data_row.get('name', 'Error')}]: {str(e)}")

            # 1. Fallback backup save to local reports/screenshots path
            ScreenshotUtil.capture_screenshot(driver, f"FlowError_{clean_name}")

            # 2. Embed critical failure snapshot context directly into Allure HTML Report tree
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"CRITICAL_FAILURE_FLOW_{clean_name}",
                attachment_type=allure.attachment_type.PNG
            )
            raise e