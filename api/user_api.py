"""
User Management API Client
Implements all User Management API endpoints with proper error handling
"""

from typing import Dict, Any, Tuple
import requests
from .base_api import BaseAPI
from common.logger import logger
from common.data_generator import data_generator


class UserAPI(BaseAPI):
    """User Management API client with all CRUD operations"""

    def __init__(self):
        super().__init__()
        self.base_endpoint = "/api/v1/users"

    def create_user(self, user_data: Dict[str, Any]) -> Tuple[requests.Response, float]:
        """
        Create a new user

        Args:
            user_data: User data containing username, email, password

        Returns:
            Tuple of (response, response_time)
        """
        try:
            return self.post(self.base_endpoint, user_data)
        except Exception as e:
            logger.log_error("create_user", f"Failed to create user: {str(e)}")
            raise

    def get_user_details(self, user_id: int) -> Tuple[requests.Response, float]:
        """
        Get user details by ID

        Args:
            user_id: User ID to retrieve

        Returns:
            Tuple of (response, response_time)
        """

        try:
            endpoint = f"{self.base_endpoint}/{user_id}"
            response, response_time = self.get(endpoint)
            return response, response_time

        except Exception as e:
            logger.log_error(
                "get_user_details", f"Failed to get user details: {str(e)}"
            )
            raise

    def update_user_email(
        self, user_id: int, email: str
    ) -> Tuple[requests.Response, float]:
        """
        Update user email address

        Args:
            user_id: User ID to update
            email: New email address

        Returns:
            Tuple of (response, response_time)
        """

        try:
            endpoint = f"{self.base_endpoint}/{user_id}"
            update_data = {"email": email}
            return self.put(endpoint, update_data)

        except Exception as e:
            logger.log_error(
                "update_user_email", f"Failed to update user email: {str(e)}"
            )
            raise

    def delete_user(self, user_id: int) -> Tuple[requests.Response, float]:
        """
        Delete user by ID

        Args:
            user_id: User ID to delete

        Returns:
            Tuple of (response, response_time)
        """

        try:
            endpoint = f"{self.base_endpoint}/{user_id}"
            return self.delete(endpoint)

        except Exception as e:
            logger.log_error("delete_user", f"Failed to delete user: {str(e)}")
            raise

    def batch_query_users(
        self, page: int = 1, size: int = 10, keyword: str = None
    ) -> Tuple[requests.Response, float]:
        """
        Batch query users with pagination and filtering

        Args:
            page: Page number (default: 1)
            size: Page size (default: 10)
            keyword: Search keyword (optional)

        Returns:
            Tuple of (response, response_time)
        """
        try:
            params = {"page": page, "size": size}
            if keyword:
                params["keyword"] = keyword

            response, response_time = self.get(self.base_endpoint, params)
            return response, response_time

        except Exception as e:
            logger.log_error("batch_query_users", f"Failed to query users: {str(e)}")
            raise

    def cleanup_created_users(self):
        """Cleanup all created users during testing"""
        created_ids = data_generator.get_created_user_ids()

        for user_id in created_ids:
            try:
                self.delete_user(user_id)
            except Exception as e:
                logger.log_error(
                    "cleanup_user", f"Failed to cleanup user {user_id}: {str(e)}"
                )
