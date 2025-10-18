"""
Test Configuration Management
Supports multi-environment switching via environment variables
"""

import os
from typing import Dict, Any


class TestConfig:
    """Centralized configuration management for API testing"""

    def __init__(self):
        self.environment = os.getenv("TEST_ENV", "test")
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration based on environment"""
        configs = {
            "test": {
                "base_url": "http://localhost:8000",
                "timeout": 30,
                "retry_attempts": 3,
                "retry_delay": 1,
                "log_level": "DEBUG",
                "mock_responses": True,
            },
            "staging": {
                "base_url": "https://staging-api.novumstudio.com",
                "timeout": 30,
                "retry_attempts": 3,
                "retry_delay": 1,
                "log_level": "INFO",
                "mock_responses": False,
            },
            "production": {
                "base_url": "https://api.novumstudio.com",
                "timeout": 30,
                "retry_attempts": 2,
                "retry_delay": 2,
                "log_level": "WARNING",
                "mock_responses": False,
            },
        }
        return configs.get(self.environment, configs["test"])

    @property
    def base_url(self) -> str:
        return self.config["base_url"]

    @property
    def timeout(self) -> int:
        return self.config["timeout"]

    @property
    def retry_attempts(self) -> int:
        return self.config["retry_attempts"]

    @property
    def retry_delay(self) -> int:
        return self.config["retry_delay"]

    @property
    def log_level(self) -> str:
        return self.config["log_level"]

    @property
    def mock_responses(self) -> bool:
        return self.config["mock_responses"]

    def get_api_endpoint(self, endpoint: str) -> str:
        """Get full API endpoint URL"""
        return f"{self.base_url}{endpoint}"

    def get_headers(self) -> Dict[str, str]:
        """Get default headers for API requests"""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "API-Test-Framework/1.0",
        }


config = TestConfig()
