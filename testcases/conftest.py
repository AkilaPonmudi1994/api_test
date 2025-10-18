from api.user_api import UserAPI
from common.data_generator import data_generator
import pytest

import allure
import json
import os
from datetime import datetime


@pytest.fixture(scope="class")
def user_api():
    """User API client fixture"""
    api = UserAPI()
    yield api
    api.cleanup()


@pytest.fixture(autouse=True)
def test_setup():
    """Setup before each test"""
    data_generator.reset_data()
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results and attach API details to Allure"""
    outcome = yield
    _report = outcome.get_result()

    # Store the result in the test item for use in fixtures
    setattr(item, "rep_" + _report.when, _report)
    # Attach API request/response details for API tests
    if hasattr(item, "instance") and hasattr(item.instance, "user_api"):
        if _report.when == "call":
            # Attach test execution details
            allure.attach(
                json.dumps(
                    {
                        "test_name": item.name,
                        "test_class": item.cls.__name__ if item.cls else "Unknown",
                        "execution_time": datetime.now().isoformat(),
                        "result": "PASSED" if _report.passed else "FAILED",
                    },
                    indent=2,
                ),
                name="test_execution_details",
                attachment_type=allure.attachment_type.JSON,
            )

            if not _report.passed:
                # Attach error details for failed tests
                allure.attach(
                    str(_report.longrepr),
                    name="test_error_details",
                    attachment_type=allure.attachment_type.TEXT,
                )


@pytest.fixture(scope="session", autouse=True)
def allure_environment():
    """Set up Allure environment information"""
    environment_info = {
        "Test Environment": os.getenv("TEST_ENV", "test"),
        "Python Version": os.sys.version,
    }

    os.makedirs("reports", exist_ok=True)
    with open("reports/environment.properties", "w") as f:
        for key, value in environment_info.items():
            f.write(f"{key}={value}\n")
