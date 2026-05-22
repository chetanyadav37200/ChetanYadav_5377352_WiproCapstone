import allure
import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config_reader import ConfigReader
from utils.logger import LogGen
from utils.csv_reader import CSVReader
from pages.home_page import HomePage
from pages.insurance_page import InsurancePage
from pages.plans_page import PlansPage
from pages.traveller_page import TravellerPage
from pages.login_popup_page import LoginPopupPage

logger = LogGen.loggen()

# ==================================================================================
#  DATA SEPARATION ENGINES
# ==================================================================================
flow_data = CSVReader.read_csv("travel_insurance_inputs.csv")[0]
passenger_data = CSVReader.read_csv("insurance_data.csv")


@pytest.fixture(scope="function")
def setup_insurance_flow(driver):
    """Fixture to handle dynamic destination navigation using layout dataset maps."""
    home_page = HomePage(driver)
    insurance_page = InsurancePage(driver)
    plans_page = PlansPage(driver)
    login_popup = LoginPopupPage(driver)

    base_url = ConfigReader.get("base_url").strip()
    driver.get(base_url)

    login_popup.close_popup_if_present()
    home_page.click_travel_insurance()

    # 1. Select destination country using config data maps
    insurance_page.select_country(flow_data["Country"])

    # 2. Extract and pass traveler counts dynamically from dataset parameters
    target_travellers = flow_data.get("Travellers", flow_data.get("travellers", "1"))
    insurance_page.select_travellers_count(target_travellers)

    # 3. Fire search submission pipeline execution
    insurance_page.click_explore_plans()

    return plans_page, TravellerPage(driver)


# ==========================================
#               NEGATIVE TEST CASES
# ==========================================

@allure.feature("Insurance Form Validations")
@allure.story("Negative Validation Checkpoints")
@pytest.mark.parametrize("data", passenger_data)
def test_neg_blank_date_of_birth(setup_insurance_flow, data):
    """Negative 1: Verify system catches empty/blank DOB entry field"""
    plans_page, traveller_page = setup_insurance_flow
    target_plan = data.get('plan_index', 1)

    with allure.step(f"Select plan index {target_plan} and navigate to traveller details form"):
        plans_page.click_buy_now(target_plan)

    with allure.step(f"Fill traveller info leaving DOB blank for user: {data['name']}"):
        logger.info(f"Executing Negative Test (Blank DOB) for user: {data['name']}. Using plan column: {target_plan}")
        traveller_page.fill_traveller_info(data['name'], "", data['gender'])
        traveller_page.fill_contact_info(data['mobile'], data['email'])
        traveller_page.complete_booking_flow()

    with allure.step("Validate Blank DOB validation error on screen"):
        error_text = traveller_page.get_dob_error_message()
        assert error_text == "Please enter valid Date of Birth", f"Unexpected error text: {error_text}"


@allure.feature("Insurance Form Validations")
@allure.story("Negative Validation Checkpoints")
@pytest.mark.parametrize("data", passenger_data)
def test_neg_blank_mobile_number(setup_insurance_flow, data):
    """Negative 2: Verify validation failure when Mobile field is completely empty"""
    plans_page, traveller_page = setup_insurance_flow
    target_plan = data.get('plan_index', 1)

    with allure.step(f"Select plan index {target_plan} and navigate to traveller details form"):
        plans_page.click_buy_now(target_plan)

    with allure.step(f"Fill traveller info leaving Mobile blank for user: {data['name']}"):
        logger.info(f"Executing Negative Test (Blank Mobile) for user: {data['name']}. Using plan column: {target_plan}")
        traveller_page.fill_traveller_info(data['name'], data['dob'], data['gender'])
        traveller_page.fill_contact_info("", data['email'])
        traveller_page.complete_booking_flow()

    with allure.step("Validate Blank Mobile validation error on screen"):
        error_text = traveller_page.get_mobile_error_message()
        assert error_text == "Please enter mobile number", f"Unexpected error text: {error_text}"


@allure.feature("Insurance Form Validations")
@allure.story("Negative Validation Checkpoints")
@pytest.mark.parametrize("data", passenger_data)
def test_neg_invalid_mobile_number(setup_insurance_flow, data):
    """Negative 3: Verify error flag for structurally invalid mobile numbers"""
    plans_page, traveller_page = setup_insurance_flow
    target_plan = data.get('plan_index', 1)

    with allure.step(f"Select plan index {target_plan} and navigate to traveller details form"):
        plans_page.click_buy_now(target_plan)

    with allure.step(f"Fill traveller info with invalid Mobile sequence for user: {data['name']}"):
        logger.info(f"Executing Negative Test (Invalid Mobile) for user: {data['name']}. Using plan column: {target_plan}")
        traveller_page.fill_traveller_info(data['name'], data['dob'], data['gender'])
        traveller_page.fill_contact_info("12345", data['email'])
        traveller_page.complete_booking_flow()

    with allure.step("Validate Invalid Mobile format validation error on screen"):
        error_text = traveller_page.get_mobile_error_message()
        assert error_text == "Please enter valid Mobile No.", f"Unexpected error text: {error_text}"


# ==========================================
#               POSITIVE TEST CASES
# ==========================================

@allure.feature("Insurance Form Validations")
@allure.story("Positive Presentation Checkpoints")
def test_pos_assert_choose_your_plans_page(setup_insurance_flow):
    """Positive 1: Verify 'Choose your plans' UI presentation layers load successfully"""
    plans_page, _ = setup_insurance_flow

    with allure.step("Assert choose your plans page is properly loaded"):
        logger.info("Executing Positive Test: Asserting Choose Plans Grid Matrix.")
        is_present = plans_page.is_choose_plan_present()
        assert is_present, "Error: Plans matrix grid failed to load properly!"


@allure.feature("Insurance Form Validations")
@allure.story("Positive Presentation Checkpoints")
def test_pos_assert_international_insurance_branding(setup_insurance_flow):
    """Positive 2: Validate presence of 'International Travel + Medical Insurance' policy line"""
    plans_page, _ = setup_insurance_flow
    driver_instance = plans_page.driver

    # Instantiate the page object where the dynamic header locator resides natively
    insurance_page = InsurancePage(driver_instance)

    with allure.step("Validate visibility of international medical insurance policy context text headers"):
        logger.info("Executing Positive Test: Confirming International Travel + Medical Insurance Header Context.")

        # Explicitly wait to guarantee the DOM tree completely renders the element matching your image layout
        element = WebDriverWait(driver_instance, 10).until(
            EC.visibility_of_element_located(insurance_page.INSURANCE_PAGE_CHECKMARK)
        )
        is_displayed = element.is_displayed()
        assert is_displayed, "Policy banner for 'International Travel + Medical Insurance' is missing."


@allure.feature("Insurance Form Validations")
@allure.story("Positive Presentation Checkpoints")
def test_pos_assert_traveller_details_form_view(setup_insurance_flow):
    """Positive 3: Verify transition to Checkout page and user Profile Info Form"""
    plans_page, traveller_page = setup_insurance_flow

    with allure.step("Click buy now on first plan card layout matrix layer"):
        plans_page.click_buy_now(1)

    with allure.step("Verify traveler contact form layout layer view visibility"):
        logger.info("Executing Positive Test: Verifying Traveler details review block visibility.")
        is_open = traveller_page.is_traveller_page_open()
        is_header_present = traveller_page.is_traveller_header_present()

        assert is_open, "Checkout input profile screen failed to open."
        assert is_header_present, "Travellers form header section component missing."


@allure.feature("Insurance Form Validations")
@allure.story("Positive Presentation Checkpoints")
@pytest.mark.parametrize("data", passenger_data)
def test_pos_complete_valid_form_submission(setup_insurance_flow, data):
    """Positive 4: Complete end-to-end injection block with completely valid profile metrics"""
    plans_page, traveller_page = setup_insurance_flow
    driver_instance = plans_page.driver
    login_popup = LoginPopupPage(driver_instance)

    target_plan = data.get('plan_index', 1)

    with allure.step(f"Select target plan position index card: {target_plan}"):
        plans_page.click_buy_now(target_plan)

    with allure.step(f"Fill and complete valid form fields data stream for user: {data['name']}"):
        logger.info(f"Executing Positive Test: Processing full valid validation path for {data['name']}. Using plan column: {target_plan}")
        traveller_page.fill_traveller_info(data['name'], data['dob'], data['gender'])
        traveller_page.fill_contact_info(data['mobile'], data['email'])
        traveller_page.complete_booking_flow()
        time.sleep(2.5)

    with allure.step("Verify that authentication intercept screen has successfully triggered without form errors"):
        if login_popup.is_login_popup_displayed():
            logger.info("Form passed validation checkpoints; OTP authentication module triggered.")
            assert True
        else:
            assert not traveller_page.has_validation_errors(), "Form submission failed due to unexpected active validation errors on the page."