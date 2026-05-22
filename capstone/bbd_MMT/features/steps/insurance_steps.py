import time
import allure
import re
from behave import given, when, then, use_step_matcher

from utils.config_reader import ConfigReader
from utils.logger import LogGen
from utils.waits import WaitUtils

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
#  POSITIVE STEP IMPLEMENTATIONS
# ==================================================================================

@then('the choice of insurance plan grid matrix structure must load successfully')
def step_impl(context):
    logger.info("Executing BDD Positive Test: Asserting Choose Plans Grid Matrix.")
    is_present = context.plans_page.is_choose_plan_present()
    assert is_present, "Error: Plans matrix grid failed to load properly!"


@then('the visibility of international travel and medical insurance policy headers must be confirmed')
def step_impl(context):
    logger.info("Executing BDD Positive Test: Confirming International Travel Policy Header Presence.")
    element = WaitUtils.wait_for_element_visible(context.driver, context.insurance_page.INSURANCE_PAGE_CHECKMARK)
    assert element.is_displayed(), "Policy banner for 'International Travel + Medical Insurance' is missing."


# ==================================================================================
#  DATA-DRIVEN OUTLINE NEGATIVE STEP IMPLEMENTATIONS
# ==================================================================================

@when('the user configures the flow map targeting destination country "{country}"')
def step_impl(context, country):
    context.insurance_page.select_country(country)


@when('the user configures traveler volume parameters for "{travellers}" rows')
def step_impl(context, travellers):
    context.insurance_page.select_travellers_count(travellers)


@when('the user executes plan searches and clicks buy now on plan card position "{plan_index}"')
def step_impl(context, plan_index):
    context.insurance_page.click_explore_plans()
    time.sleep(2.5)  # Safe Single-Page Application (SPA) layout change gap
    assert context.plans_page.is_choose_plan_present(), "Plans matrix grid failed to load!"
    context.plans_page.click_buy_now(plan_index)
    time.sleep(2.0)


# ----------------------------------------------------------------------------------
# REGEX STEP MATCHING SECTION (For safe dynamic parameter strings)
# ----------------------------------------------------------------------------------
use_step_matcher("re")


@when(
    r'the user attempts info validation using name (?P<name>.*?), dob (?P<dob>.*?), gender (?P<gender>.*?), mobile (?P<mobile>.*?), and email (?P<email>.*)')
def step_impl(context, name, dob, gender, mobile, email):
    """
    Advanced Regex Matcher: Captures values seamlessly even when parameters
    like 'dob' or 'mobile' are left completely empty inside the Gherkin row text block.
    """
    assert context.traveller_page.is_traveller_page_open(), "Checkout form tree missing!"

    # Strip lingering double quotes if passed directly from Gherkin fields
    clean_name = str(name).replace('"', '').strip()
    clean_dob = str(dob).replace('"', '').strip()
    clean_gender = str(gender).replace('"', '').strip()
    clean_mobile = str(mobile).replace('"', '').strip()
    clean_email = str(email).replace('"', '').strip()

    logger.info(f"Regex Engine Active: Validating profile form parameters for [{clean_name}]")

    # Input data using cleaned text strings
    context.traveller_page.fill_traveller_info(clean_name, clean_dob, clean_gender)
    context.traveller_page.fill_contact_info(clean_mobile, clean_email)
    context.traveller_page.complete_booking_flow()


# Restore the native parse step matcher so standard strings parse normally
use_step_matcher("parse")


# ----------------------------------------------------------------------------------


@then(
    'the system field tracking validation engine must surface the error "{expected_error}" for field type "{error_type}"')
def step_impl(context, expected_error, error_type):
    if error_type.strip().upper() == "DOB":
        ui_error_text = context.traveller_page.get_dob_error_message()
    else:
        ui_error_text = context.traveller_page.get_mobile_error_message()

    assert ui_error_text == expected_error, f"Validation mismatch! Found UI message: '{ui_error_text}'"


# ==================================================================================
#  END-TO-END FUNCTIONAL BATCH EXECUTIONS (NATIVE GHERKIN PARSING)
# ==================================================================================

@when('the user processes the following valid customer registration profile:')
def step_impl(context):
    """Parses the standalone data grid straight from the feature file context."""
    context.e2e_data = context.table.rows[0]
    logger.info(f"Loaded target execution credentials for: {context.e2e_data['name']} via native data-table.")


@when('the system fully automates the valid profile registration stream pipeline')
def step_impl(context):
    data = context.e2e_data
    config_mobile = ConfigReader.get("mobile_number").strip()

    # Run full navigation loop
    context.insurance_page.select_country(data["Country"])
    context.insurance_page.select_travellers_count(data["Travellers"])
    context.insurance_page.click_explore_plans()
    time.sleep(2.5)

    context.plans_page.click_buy_now(data['plan_index'])
    time.sleep(2.0)

    context.traveller_page.fill_traveller_info(data['name'], data['dob'], data['gender'])
    context.traveller_page.fill_contact_info(data['mobile'], data['email'])
    context.traveller_page.complete_booking_flow()
    time.sleep(2.5)

    if context.login_popup.is_login_popup_displayed():
        allure.attach(
            context.driver.get_screenshot_as_png(),
            name="BDD_Step_Authentication_OTP_Prompt_Intercepted",
            attachment_type=allure.attachment_type.PNG
        )
        context.login_popup.login_with_mobile_and_wait_for_otp(config_mobile)


@then('the user profile should clear forms safely with authentication panels triggered')
def step_impl(context):
    if context.login_popup.is_login_popup_displayed():
        logger.info("End-to-End complete: OTP form verification intercept captured cleanly.")
        assert True
    else:
        assert not context.traveller_page.has_validation_errors(), "The automation stream terminated due to unhandled form errors."