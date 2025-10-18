"""
Base API Client with Mocking Support
Provides HTTP client functionality with retry mechanisms and comprehensive error handling
"""

import requests
import time
import json
from typing import Dict, Any, Tuple
from config.test_config import config
from common.logger import logger
from common.data_generator import data_generator


class BaseAPI:
    """Base API client with retry mechanisms and error handling"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(config.get_headers())
        self.mock_responses = {}
        self._load_mock_data()

    def _load_mock_data(self):
        """Load mock response data from JSON files"""
        try:
            expected_data = data_generator.load_test_data("data/api_responses.json")

            self.mock_responses.update(expected_data)

        except Exception as e:
            logger.log_error("mock_data_load", f"Failed to load mock data: {str(e)}")

    def _make_request(
        self, method: str, endpoint: str, **kwargs
    ) -> Tuple[requests.Response, float]:
        """Make HTTP request with retry logic and timing"""
        url = config.get_api_endpoint(endpoint)
        start_time = time.time()

        # Log request
        logger.log_api_request(
            method,
            url,
            kwargs.get("headers"),
            kwargs.get("json"),
            kwargs.get("params"),
        )

        # Handle mocking if enabled
        if config.mock_responses:
            response = self._get_mock_response(method, endpoint, **kwargs)
            response_time = time.time() - start_time
            logger.log_api_response(
                response.status_code,
                response.json() if response.content else {},
                response_time,
            )
            return response, response_time

        # Make actual HTTP request with retry logic
        for attempt in range(config.retry_attempts):
            try:
                response = self.session.request(
                    method, url, timeout=config.timeout, **kwargs
                )
                response_time = time.time() - start_time

                # Log response
                try:
                    response_data = response.json()
                except Exception:
                    response_data = {"content": response.text}

                logger.log_api_response(
                    response.status_code, response_data, response_time
                )
                return response, response_time

            except requests.exceptions.RequestException as e:
                if attempt == config.retry_attempts - 1:
                    logger.log_error(
                        "api_request",
                        f"Request failed after {config.retry_attempts} attempts: {str(e)}",
                    )
                    raise
                else:
                    logger.log_error(
                        "api_request", f"Request attempt {attempt + 1} failed: {str(e)}"
                    )
                    time.sleep(config.retry_delay)

        # This should never be reached
        raise Exception("Unexpected error in request handling")

    def _get_mock_response(
        self, method: str, endpoint: str, **kwargs
    ) -> requests.Response:
        """Generate mock response based on request"""
        # Create a mock response object
        mock_response = requests.Response()
        mock_response.status_code = 200

        # Determine response based on endpoint and method
        if method == "POST" and endpoint == "/api/v1/users":
            # Create user endpoint
            user_data = kwargs.get("json", {})

            # Check for duplicate username
            if self._check_duplicate_username(user_data.get("username")):
                mock_response.status_code = 409
                mock_response._content = json.dumps(
                    self.mock_responses["duplicate_username"]
                ).encode()
                return mock_response

            # Check for duplicate email
            if self._check_duplicate_email(user_data.get("email")):
                mock_response.status_code = 409
                mock_response._content = json.dumps(
                    self.mock_responses["duplicate_email"]
                ).encode()
                return mock_response

            # Validate user data
            if self._is_valid_user_data(user_data):
                response_format = self.mock_responses["create_user_success"]
                new_id = data_generator.generate_unique_id()
                data_generator.add_user_data(new_id, user_data)
                response_format["data"] = {
                    "id": new_id,
                    "username": user_data["username"],
                }

                mock_response._content = json.dumps(response_format).encode()
            else:
                # Determine specific validation error
                error_response = self._get_validation_error(user_data)
                mock_response.status_code = error_response["code"]
                mock_response._content = json.dumps(error_response).encode()

        elif method == "GET" and endpoint.startswith("/api/v1/users/"):
            # Get user details endpoint
            user_id = endpoint.split("/")[-1]
            if (
                user_id.isdigit()
                and int(user_id) in data_generator.get_created_user_ids()
            ):  # Valid user IDs
                response_format = self.mock_responses["get_user_success"]
                user_data = data_generator.get_created_user_data(int(user_id))
                response_format["data"] = user_data
                mock_response._content = json.dumps(response_format).encode()
            else:
                mock_response.status_code = 404
                mock_response._content = json.dumps(
                    self.mock_responses["user_not_found"]
                ).encode()

        elif method == "PUT" and endpoint.startswith("/api/v1/users/"):
            # Update user endpoint
            user_id = endpoint.split("/")[-1]
            update_data = kwargs.get("json", {})
            is_found = (
                user_id.isdigit()
                and int(user_id) in data_generator.get_created_user_ids()
            )
            if is_found and self._is_valid_email(update_data.get("email")):
                response_format = self.mock_responses["update_user_success"]
                user_data = data_generator.get_created_user_data(int(user_id))
                user_data["email"] = update_data.get("email")
                response_format["data"] = user_data
                mock_response._content = json.dumps(response_format).encode()
            else:
                res_code = 400
                response_format = self.mock_responses["invalid_parameters"]
                if (
                    user_id.isdigit()
                    and int(user_id) not in data_generator.get_created_user_ids()
                ):
                    res_code = 404
                    response_format = self.mock_responses["user_not_found"]
                mock_response.status_code = res_code

                mock_response._content = json.dumps(response_format).encode()

        elif method == "DELETE" and endpoint.startswith("/api/v1/users/"):
            # Delete user endpoint
            user_id = endpoint.split("/")[-1]
            if (
                user_id.isdigit()
                and int(user_id) in data_generator.get_created_user_ids()
            ):
                mock_response.status_code = 200
                mock_response._content = json.dumps(
                    self.mock_responses["delete_user_success"]
                ).encode()
                data_generator.remove_user(user_id)
            else:
                mock_response.status_code = 404
                mock_response._content = json.dumps(
                    self.mock_responses["user_not_found"]
                ).encode()

        elif method == "GET" and endpoint == "/api/v1/users":
            # Batch query users endpoint
            params = kwargs.get("params", {})
            if self._is_valid_query_params(params):
                mock_response._content = json.dumps(
                    self.mock_responses["batch_query_success"]
                ).encode()
            else:
                mock_response.status_code = 400
                mock_response._content = json.dumps(
                    self.mock_responses["invalid_parameters"]
                ).encode()

        else:
            # Unknown endpoint
            mock_response.status_code = 404
            mock_response._content = json.dumps(
                self.mock_responses["user_not_found"]
            ).encode()

        return mock_response

    def _is_valid_user_data(self, user_data: Dict[str, Any]) -> bool:
        """Validate user data for creation"""
        required_fields = ["username", "email", "password"]
        valid = True

        for field in required_fields:
            if (
                field not in user_data
                or not isinstance(user_data[field], str)
                or not user_data[field].strip()
            ):
                valid = False
                break

            if field == "email" and not self._is_valid_email(user_data[field]):
                valid = False
                break

            if field == "password" and not self._is_valid_password(user_data[field]):
                valid = False
                break

            if field == "username" and not self._is_valid_username(user_data[field]):
                valid = False
                break

        return valid

    def _is_valid_email(self, email: str) -> bool:
        """Validate email format"""
        if not email or len(email) > 254:  # RFC 5321 limit
            return False
        if email.count("@") != 1:
            return False
        local, domain = email.split("@")
        if not local or not domain or "." not in domain:
            return False
        return True

    def _is_valid_password(self, password: str) -> bool:
        """Validate password strength"""
        if not password or len(password) < 8:
            return False
        # Check for spaces only
        if password.strip() == "":
            return False
        return True

    def _is_valid_username(self, username: str) -> bool:
        """Validate username format"""
        if not username or len(username) > 50:  # Reasonable limit
            return False
        # Check for special characters (allow only alphanumeric and underscore)
        import re

        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            return False
        return True

    def _is_valid_query_params(self, params: Dict[str, Any]) -> bool:
        """Validate query parameters"""
        page = params.get("page", 1)
        size = params.get("size", 10)
        return (
            isinstance(page, int)
            and page > 0
            and isinstance(size, int)
            and 0 < size <= 100
        )

    def _check_duplicate_username(self, username: str) -> bool:
        """Check if username already exists"""
        if not username:
            return False
        existing_users = data_generator.get_created_user_ids()
        for user_id in existing_users:
            user_data = data_generator.get_created_user_data(user_id)
            if user_data.get("username") == username:
                return True
        return False

    def _check_duplicate_email(self, email: str) -> bool:
        """Check if email already exists"""
        if not email:
            return False
        existing_users = data_generator.get_created_user_ids()
        for user_id in existing_users:
            user_data = data_generator.get_created_user_data(user_id)
            if user_data.get("email") == email:
                return True
        return False

    def _get_validation_error(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get specific validation error based on user data"""
        username = user_data.get("username", "")
        email = user_data.get("email", "")
        password = user_data.get("password", "")

        # Check username issues
        if not username or not username.strip():
            return self.mock_responses["invalid_parameters"]
        if len(username) > 50:
            return self.mock_responses["username_too_long"]
        if not self._is_valid_username(username):
            return self.mock_responses["invalid_username_format"]

        # Check email issues
        if not email or not email.strip():
            return self.mock_responses["invalid_parameters"]
        if len(email) > 254:
            return self.mock_responses["email_too_long"]
        if not self._is_valid_email(email):
            return self.mock_responses["invalid_parameters"]

        # Check password issues
        if not password or not password.strip():
            return self.mock_responses["invalid_parameters"]
        if not self._is_valid_password(password):
            return self.mock_responses["password_too_weak"]

        # Default to invalid parameters
        return self.mock_responses["invalid_parameters"]

    def get(
        self, endpoint: str, params: Dict[str, Any] = None, **kwargs
    ) -> Tuple[requests.Response, float]:
        """GET request"""
        return self._make_request("GET", endpoint, params=params, **kwargs)

    def post(
        self, endpoint: str, data: Dict[str, Any] = None, **kwargs
    ) -> Tuple[requests.Response, float]:
        """POST request"""
        return self._make_request("POST", endpoint, json=data, **kwargs)

    def put(
        self, endpoint: str, data: Dict[str, Any] = None, **kwargs
    ) -> Tuple[requests.Response, float]:
        """PUT request"""
        return self._make_request("PUT", endpoint, json=data, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Tuple[requests.Response, float]:
        """DELETE request"""
        return self._make_request("DELETE", endpoint, **kwargs)

    def cleanup(self):
        """Cleanup resources"""
        self.session.close()
