import time
import allure
import os
from behave import given, when, then

from utils.config_reader import ConfigReader
from utils.logger import LogGen
from utils.waits import WaitUtils
from utils.csv_reader import CsvReader

from pages.home_page import HomePage
from pages.insurance_page import InsurancePage
from pages.plans_page import PlansPage
from pages.traveller_page import TravellerPage
from pages.login_popup_page import LoginPopupPage

logger = LogGen.loggen()


# ==================================================================================
#  BACKGROUND STEP IMPLEMENTATIONS
# ==================================================================================

@given('the user opens the corporate travel portal application homepage')
def step_impl(context):
    if not hasattr(context, 'base_url'):
        try:
            context.base_url = ConfigReader.get_base_url()
        except Exception:
            context.base_url = "https://www.makemytrip.com/"
    context.driver.get(context.base_url)


@given('the user dismisses initial overlay login alerts if present')
def step_impl(context):
    context.login_popup = LoginPopupPage(context.driver)
    context.home_page = HomePage(context.driver)
    context.login_popup.close_popup_if_present()


@when('the user navigates into the Travel Insurance matrix panel page')
def step_impl(context):
    context.home_page.click_travel_insurance()
    context.insurance_page = InsurancePage(context.driver)
    context.plans_page = PlansPage(context.driver)
    context.traveller_page = TravellerPage(context.driver)


# ==================================================================================
#  GLOBAL DATA INJECTOR (Reads for both Feature Files)
# ==================================================================================

@when('the user loads test metrics from row "{row_index}" inside CSV file "{filepath}"')
def step_impl(context, row_index, filepath):
    logger.info(f"Accessing CSV Data Layer: Row [{row_index}] via [{filepath}]")
    context.csv_data = CsvReader.get_test_data(filepath, row_index)
    context.e2e_data = context.csv_data


# ==================================================================================
#  DATA CONFIGURATOR GLUE STEPS
# ==================================================================================

@when('the user configures the flow map targeting destination country from data')
def step_impl(context):
    if not hasattr(context, 'insurance_page') or context.insurance_page is None:
        context.insurance_page = InsurancePage(context.driver)
    context.insurance_page.select_country(context.csv_data["Country"])


@when('the user configures traveler volume parameters from data')
def step_impl(context):
    if not hasattr(context, 'insurance_page') or context.insurance_page is None:
        context.insurance_page = InsurancePage(context.driver)
    context.insurance_page.select_travellers_count(context.csv_data["Travellers"])


@when('the user clicks the explore plans button to execute searches')
def step_impl(context):
    context.insurance_page.click_explore_plans()
    time.sleep(4.0)


@when('the user executes plan searches and clicks buy now on plan card from data')
def step_impl(context):
    if not hasattr(context, 'plans_page') or context.plans_page is None:
        context.plans_page = PlansPage(context.driver)
    context.insurance_page.click_explore_plans()
    time.sleep(4.0)
    assert context.plans_page.is_choose_plan_present(), "Plans matrix grid failed to load!"
    context.plans_page.click_buy_now(context.csv_data["plan_index"])
    time.sleep(2.0)


# ==================================================================================
#  INPUT DRIVER AND INJECTION LOGIC
# ==================================================================================

@when('the user injects valid profile fields from loaded data mapping')
def step_impl(context):
    data = context.csv_data
    context.traveller_page.fill_traveller_info(data["name"], data["dob"], data["gender"])
    context.traveller_page.fill_contact_info(data["mobile"], data["email"])
    context.traveller_page.complete_booking_flow()
    time.sleep(2.5)


@when('the user attempts context dynamic info validations on fields')
def step_impl(context):
    data = context.csv_data
    assert context.traveller_page.is_traveller_page_open(), "Checkout form missing!"

    clean_dob = data["dob"] if data["dob"] else ""
    clean_mobile = data["mobile"] if data["mobile"] else ""

    context.traveller_page.fill_traveller_info(data["name"], clean_dob, data["gender"])
    context.traveller_page.fill_contact_info(clean_mobile, data["email"])
    context.traveller_page.complete_booking_flow()


@when('the system fully automates the valid profile registration stream pipeline')
def step_impl(context):
    data = context.e2e_data
    context.insurance_page.select_country(data["Country"])
    context.insurance_page.select_travellers_count(data["Travellers"])
    context.insurance_page.click_explore_plans()
    time.sleep(4.0)
    context.plans_page.click_buy_now(data['plan_index'])
    time.sleep(2.0)
    context.traveller_page.fill_traveller_info(data['name'], data['dob'], data['gender'])
    context.traveller_page.fill_contact_info(data['mobile'], data['email'])
    context.traveller_page.complete_booking_flow()
    time.sleep(2.5)


# ==================================================================================
#  AUXILIARY REPORT ATTACHMENT UTILITY BLOCK
# ==================================================================================

def attach_step_artifacts(context, name_suffix):
    """Safely extracts live runtime logs and window graphics straight to Allure layers."""
    try:
        # 1. Attach Live Binary Screenshot Data Stream
        allure.attach(
            context.driver.get_screenshot_as_png(),
            name=f"✅_SUCCESS_VIEW_{name_suffix.upper()}",
            attachment_type=allure.attachment_type.PNG
        )

        # 2. Attach Current Automation Log Entries File State
        log_path = "logs/automation.log"
        if os.path.exists(log_path):
            allure.attach.file(
                log_path,
                name=f"📋_STEP_RUN_LOGS_{name_suffix.upper()}",
                attachment_type=allure.attachment_type.TEXT
            )
    except Exception as e:
        logger.error(f"Failed to attach reporting artifacts to Allure: {str(e)}")


# ==================================================================================
#  VALIDATION LAYER ASSERTIONS (WITH INTEGRATED MEDIA & LOG INJECTIONS)
# ==================================================================================

@then('the choice of insurance plan grid matrix structure must load successfully')
def step_impl(context):
    if not hasattr(context, 'plans_page') or context.plans_page is None:
        context.plans_page = PlansPage(context.driver)

    grid_rendered = False
    for attempt in range(5):
        if context.plans_page.is_choose_plan_present():
            grid_rendered = True
            break
        time.sleep(3.0)
    assert grid_rendered, "Plans matrix grid failed to load."

    # Attach Artifact Data Streams on Pass
    attach_step_artifacts(context, "plan_grid_matrix")


@then('the visibility of international travel and medical insurance policy headers must be confirmed')
def step_impl(context):
    element = WaitUtils.wait_for_element_visible(context.driver, context.insurance_page.INSURANCE_PAGE_CHECKMARK)
    assert element.is_displayed(), "Policy header banner verification broken."

    # Attach Artifact Data Streams on Pass
    attach_step_artifacts(context, "policy_header_banner")


@then('the traveler contact form layout layer view visibility should be confirmed')
def step_impl(context):
    assert context.traveller_page.is_traveller_page_open(), "Traveler checkout screen unavailable."

    # Attach Artifact Data Streams on Pass
    attach_step_artifacts(context, "traveller_form_layout")


@then('the system field tracking validation engine must surface the expected error from data')
def step_impl(context):
    data = context.csv_data
    if data["Error_Type"].strip().upper() == "DOB":
        ui_error_text = context.traveller_page.get_dob_error_message()
    else:
        ui_error_text = context.traveller_page.get_mobile_error_message()
    assert ui_error_text == data["expected_error"], f"Validation mismatch! Found: '{ui_error_text}'"

    # Attach Artifact Data Streams on Pass
    attach_step_artifacts(context, f"validation_error_{data['Error_Type'].strip().lower()}")


@then('the authentication intercept overlay login screen should be displayed without form errors')
def step_impl(context):
    if context.login_popup.is_login_popup_displayed():
        assert True
    else:
        assert not context.traveller_page.has_validation_errors(), "Unexpected validation block locked form."

    # Attach Artifact Data Streams on Pass
    attach_step_artifacts(context, "authentication_intercept")


# ==================================================================================
#  E2E COMPATIBILITY FLOWS
# ==================================================================================

@then('the user profile should clear forms safely with authentication panels triggered')
def step_impl(context):
    if context.login_popup.is_login_popup_displayed():
        assert True
    else:
        assert not context.traveller_page.has_validation_errors(), "Automation failed over active form error warnings."

    # Attach Artifact Data Streams on Pass
    attach_step_artifacts(context, "e2e_authentication_panels")