
import os
import shutil
from datetime import datetime
from utils.logger import LogGen

logger = LogGen.loggen()

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
logger.info("========================================")
logger.info("AUTOMATION EXECUTION STARTED")

# Clean Old Allure Results
if os.path.exists("reports/allure-results"):
    logger.info("Deleting old allure-results folder")
    shutil.rmtree("reports/allure-results")

# Clean Old Allure Report
if os.path.exists("reports/allure-report"):
    logger.info("Deleting old allure-report folder")
    shutil.rmtree("reports/allure-report")

# Execute Behave Tests (targeting e2e for now)
logger.info("Starting Behave Test Execution")
behave_status = os.system("behave")
logger.info(f"Behave Execution Completed with status code : {behave_status}")

# Generate Allure HTML Report
logger.info("Generating Allure HTML Report")
allure_generate_status = os.system(
    "allure generate reports/allure-results -o reports/allure-report --clean"
)
logger.info(f"Allure Report Generated with status code : {allure_generate_status}")
logger.info("AUTOMATION EXECUTION COMPLETED")
logger.info("========================================")