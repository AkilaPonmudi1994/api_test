"""
Custom Assertion Helpers
Provides comprehensive assertion methods for API response validation
"""

import json
from typing import Dict, Any
from .logger import logger


class APIAssertions:
    """Custom assertion methods for API testing"""

    @staticmethod
    def assert_status_code(response, expected_code: int, message: str = None):
        """Assert HTTP status code"""
        actual_code = response.status_code
        passed = actual_code == expected_code

        logger.log_assertion(
            "status_code",
            expected_code,
            actual_code,
            passed,
            message or f"Expected status code {expected_code}, got {actual_code}",
        )

        assert passed, (
            f"Status code assertion failed: Expected {expected_code}, got {actual_code}"
        )

    @staticmethod
    def assert_response_structure(response, expected_structure: Dict[str, Any]):
        """Assert response has expected JSON structure"""
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            assert False, "Response is not valid JSON"

        def _assert_structure(actual: Any, expected: Dict[str, Any], path: str = ""):
            for key, expected_type in expected.items():
                current_path = f"{path}.{key}" if path else key

                if key not in actual:
                    assert False, (
                        f"Missing key '{key}' in response at path '{current_path}'"
                    )

                if isinstance(expected_type, dict):
                    if not isinstance(actual[key], dict):
                        assert False, (
                            f"Expected dict at '{current_path}', got {type(actual[key])}"
                        )
                    _assert_structure(actual[key], expected_type, current_path)
                elif expected_type == "string":
                    assert isinstance(actual[key], str), (
                        f"Expected string at '{current_path}', got {type(actual[key])}"
                    )
                elif expected_type == "int":
                    assert isinstance(actual[key], int), (
                        f"Expected int at '{current_path}', got {type(actual[key])}"
                    )
                elif expected_type == "null":
                    assert actual[key] is None, (
                        f"Expected null at '{current_path}', got {actual[key]}"
                    )

        _assert_structure(response_data, expected_structure)
        logger.log_assertion(
            "response_structure", expected_structure, response_data, True
        )

    @staticmethod
    def assert_response_code(response, expected_code: int):
        """Assert API response code field"""
        response_data = response.json()
        actual_code = response_data.get("code")

        passed = actual_code == expected_code
        logger.log_assertion(
            "response_code",
            expected_code,
            actual_code,
            passed,
            f"Expected API code {expected_code}, got {actual_code}",
        )

        assert passed, (
            f"API response code assertion failed: Expected {expected_code}, got {actual_code}"
        )

    @staticmethod
    def assert_response_message(response, expected_message: str):
        """Assert API response message"""
        response_data = response.json()
        actual_message = response_data.get("msg")

        passed = actual_message == expected_message
        logger.log_assertion(
            "response_message",
            expected_message,
            actual_message,
            passed,
            f"Expected message '{expected_message}', got '{actual_message}'",
        )

        assert passed, (
            f"Response message assertion failed: Expected '{expected_message}', got '{actual_message}'"
        )

    @staticmethod
    def assert_user_data(response, expected_user: Dict[str, Any]):
        """Assert user data in response matches expected values"""
        response_data = response.json()
        user_data = response_data.get("data", {})

        for key, expected_value in expected_user.items():
            actual_value = user_data.get(key)
            passed = actual_value == expected_value

            logger.log_assertion(
                f"user_data.{key}",
                expected_value,
                actual_value,
                passed,
                f"User data field '{key}' assertion",
            )

            assert passed, (
                f"User data assertion failed for '{key}': Expected '{expected_value}', got '{actual_value}'"
            )

    @staticmethod
    def assert_pagination_data(
        response, expected_total: int = None, expected_count: int = None
    ):
        """Assert pagination data in batch query response"""
        response_data = response.json()
        data = response_data.get("data", {})

        if expected_total is not None:
            actual_total = data.get("total")
            passed = actual_total == expected_total
            logger.log_assertion(
                "pagination_total", expected_total, actual_total, passed
            )
            assert passed, (
                f"Total count assertion failed: Expected {expected_total}, got {actual_total}"
            )

        if expected_count is not None:
            actual_count = len(data.get("list", []))
            passed = actual_count == expected_count
            logger.log_assertion(
                "pagination_count", expected_count, actual_count, passed
            )
            assert passed, (
                f"List count assertion failed: Expected {expected_count}, got {actual_count}"
            )

    @staticmethod
    def assert_error_response(
        response, expected_error_code: int, expected_message: str = None
    ):
        """Assert error response structure and content"""
        # Assert HTTP status code indicates error
        assert response.status_code >= 400, (
            f"Expected error status code, got {response.status_code}"
        )

        response_data = response.json()

        # Assert error response structure
        assert "code" in response_data, "Error response missing 'code' field"
        assert "msg" in response_data, "Error response missing 'msg' field"
        assert response_data.get("data") is None, (
            "Error response should have null data field"
        )

        # Assert error code
        actual_code = response_data.get("code")
        passed = actual_code == expected_error_code
        logger.log_assertion("error_code", expected_error_code, actual_code, passed)
        assert passed, (
            f"Error code assertion failed: Expected {expected_error_code}, got {actual_code}"
        )

        # Assert error message if provided
        if expected_message:
            actual_message = response_data.get("msg")
            passed = expected_message in actual_message
            logger.log_assertion(
                "error_message", expected_message, actual_message, passed
            )
            assert passed, (
                f"Error message assertion failed: Expected '{expected_message}' in '{actual_message}'"
            )

    @staticmethod
    def assert_response_time(response_time: float, max_time: float = 5.0):
        """Assert response time is within acceptable limits"""
        passed = response_time <= max_time
        logger.log_assertion("response_time", max_time, response_time, passed)
        assert passed, (
            f"Response time assertion failed: {response_time}s exceeds maximum {max_time}s"
        )


# Global assertions instance
assertions = APIAssertions()
