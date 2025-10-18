"""
Logging Configuration
Provides configurable logging levels and structured output
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any


class StructuredLogger:
    """Structured logger for API testing with configurable levels"""

    def __init__(self, name: str, level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))

        # Create console handler with structured format
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_api_request(
        self,
        method: str,
        url: str,
        headers: Dict[str, str] = None,
        data: Dict[str, Any] = None,
        params: Dict[str, Any] = None,
    ):
        """Log API request details"""
        request_data = {
            "timestamp": datetime.now().isoformat(),
            "type": "api_request",
            "method": method,
            "url": url,
            "headers": headers or {},
            "data": data,
            "params": params,
        }
        self.logger.info(f"API Request: {json.dumps(request_data, indent=2)}")

    def log_api_response(
        self,
        status_code: int,
        response_data: Dict[str, Any],
        response_time: float = None,
    ):
        """Log API response details"""
        response_info = {
            "timestamp": datetime.now().isoformat(),
            "type": "api_response",
            "status_code": status_code,
            "response_data": response_data,
            "response_time_ms": response_time,
        }
        self.logger.info(f"API Response: {json.dumps(response_info, indent=2)}")

    def log_assertion(
        self,
        assertion_type: str,
        expected: Any,
        actual: Any,
        passed: bool,
        message: str = None,
    ):
        """Log assertion details"""
        assertion_info = {
            "timestamp": datetime.now().isoformat(),
            "type": "assertion",
            "assertion_type": assertion_type,
            "expected": expected,
            "actual": actual,
            "passed": passed,
            "message": message,
        }
        level = "INFO" if passed else "ERROR"
        self.logger.log(
            getattr(logging, level),
            f"Assertion: {json.dumps(assertion_info, indent=2)}",
        )

    def log_error(self, error_type: str, message: str, details: Dict[str, Any] = None):
        """Log error details"""
        error_info = {
            "timestamp": datetime.now().isoformat(),
            "type": "error",
            "error_type": error_type,
            "message": message,
            "details": details,
        }
        self.logger.error(f"Error: {json.dumps(error_info, indent=2)}")


# Global logger instance
logger = StructuredLogger("api_test_framework")
