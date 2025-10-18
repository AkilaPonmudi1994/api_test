"""
Dynamic Test Data Generation
Generates unique test data to avoid conflicts and ensure test independence
"""

import json
from faker import Faker
from typing import Dict, Any, List


class DataGenerator:
    """Generate dynamic test data for API testing"""

    def __init__(self):
        self.fake = Faker()
        self.test_users = []

    def load_data(self):
        self.test_users = self.load_test_data("data/test_users.json")

    def generate_unique_id(self) -> int:
        return self.fake.unique.random_int(min=10, max=50)

    def generate_unique_email(self, domain: str = "novumstudio.com") -> str:
        """Generate a unique email address"""
        email = self.fake.unique.email(domain=domain)
        return email

    def generate_user_data(self, **kwargs) -> Dict[str, Any]:
        """Generate complete user data with unique values"""
        return {
            "username": kwargs.get("username", self.fake.unique.user_name()),
            "email": kwargs.get("email", self.generate_unique_email()),
            "password": kwargs.get("password", self.fake.password(length=8)),
        }

    def generate_invalid_user_data(
        self, field_to_invalidate: str = "email"
    ) -> Dict[str, Any]:
        """Generate invalid user data for negative testing"""
        base_data = self.generate_user_data()

        if field_to_invalidate == "email":
            base_data["email"] = "invalid-email-format"
        elif field_to_invalidate == "username":
            base_data["username"] = ""
        elif field_to_invalidate == "password":
            base_data["password"] = "123"  # Too short

        return base_data

    def get_created_user_ids(self) -> List[int]:
        """Get list of created user IDs for cleanup"""
        return [user["id"] for user in self.test_users]

    def remove_user(self, user_id):
        removed_user = {}
        for user in self.test_users:
            if int(user["id"]) == int(user_id):
                removed_user = user
                self.test_users.remove(user)

        return removed_user

    def get_created_user_data(self, user_id: int) -> Dict[str, Any]:
        """Get created user data for cleanup"""
        user_id_to_data = {}
        for data in self.test_users:
            user_id_to_data[data["id"]] = data
        return user_id_to_data[user_id]

    def add_user_data(self, user_id, user_data):
        self.test_users.append({"id": user_id, **user_data})

    def reset_data(self):
        """Clear tracking data"""
        self.test_users.clear()
        self.load_data()

    def load_test_data(self, file_path: str) -> Dict[str, Any]:
        """Load test data from JSON file"""
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}


# Global data generator instance
data_generator = DataGenerator()
