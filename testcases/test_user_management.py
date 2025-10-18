"""
Comprehensive User Management API Test Suite
Covers all 5 APIs with positive and negative test cases
"""

import allure

from common.assertions import assertions
from common.data_generator import data_generator


@allure.feature("User Management API")
class TestCreateUser:
    """Test cases for Create User API"""

    @allure.story("Create User - Positive Cases")
    @allure.title("Create user with valid data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_normal(self, user_api):
        """Test creating user with valid data"""
        user_data = data_generator.generate_user_data()

        response, response_time = user_api.create_user(user_data)

        # Assertions
        assertions.assert_status_code(response, 200)
        assertions.assert_response_code(response, 200)
        assertions.assert_response_message(response, "success")
        assertions.assert_response_time(response_time, 5.0)

        # Verify response structure
        response_data = response.json()
        assert "data" in response_data
        assert "id" in response_data["data"]
        assert "username" in response_data["data"]
        assert response_data["data"]["username"] == user_data["username"]

    @allure.story("Create User - Negative Cases")
    @allure.title("Create user with missing username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_missing_username(self, user_api):
        """Test creating user with missing username"""
        user_data = data_generator.generate_invalid_user_data("username")

        response, response_time = user_api.create_user(user_data)

        # Assertions
        assertions.assert_status_code(response, 400)
        assertions.assert_response_code(response, 400)
        assertions.assert_error_response(response, 400, "Invalid parameters")
        assertions.assert_response_time(response_time, 5.0)

    @allure.story("Create User - Negative Cases")
    @allure.title("Create user with invalid email format")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_invalid_email(self, user_api):
        """Test creating user with invalid email format"""
        user_data = data_generator.generate_invalid_user_data("email")

        response, response_time = user_api.create_user(user_data)

        # Assertions
        assertions.assert_status_code(response, 400)
        assertions.assert_response_code(response, 400)
        assertions.assert_error_response(response, 400, "Invalid parameters")
        assertions.assert_response_time(response_time, 5.0)

    @allure.story("Create User - Negative Cases")
    @allure.title("Create user with short password")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_short_password(self, user_api):
        """Test creating user with password too short"""
        user_data = data_generator.generate_invalid_user_data("password")

        response, response_time = user_api.create_user(user_data)

        # Assertions
        assertions.assert_status_code(response, 400)
        assertions.assert_response_code(response, 400)
        assertions.assert_error_response(
            response, 400, "Password does not meet security requirements"
        )
        assertions.assert_response_time(response_time, 5.0)


@allure.feature("User Management API")
class TestGetUserDetails:
    """Test cases for Get User Details API"""

    @allure.story("Get User Details - Positive Cases")
    @allure.title("Get details of existing user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_details_existing(self, user_api):
        """Test getting details of existing user"""
        user_id = data_generator.get_created_user_ids()[0]

        response, response_time = user_api.get_user_details(user_id)

        # Assertions
        assertions.assert_status_code(response, 200)
        assertions.assert_response_code(response, 200)
        assertions.assert_response_message(response, "success")
        assertions.assert_response_time(response_time, 5.0)

        # Verify response structure
        response_data = response.json()
        assert "data" in response_data
        assert "id" in response_data["data"]
        assert "username" in response_data["data"]
        assert "email" in response_data["data"]

    @allure.story("Get User Details - Negative Cases")
    @allure.title("Get details of non-existent user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_details_nonexistent(self, user_api):
        """Test getting details of non-existent user"""
        user_id = 999  # Non-existent user ID

        response, response_time = user_api.get_user_details(user_id)

        # Assertions
        assertions.assert_status_code(response, 404)
        assertions.assert_response_code(response, 404)
        assertions.assert_error_response(response, 404, "User not found")
        assertions.assert_response_time(response_time, 5.0)

    @allure.story("Get User Details - Negative Cases")
    @allure.title("Get details with invalid user ID format")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_details_invalid_id(self, user_api):
        """Test getting details with invalid user ID format"""
        user_id = "invalid_id"  # Invalid user ID format

        response, response_time = user_api.get_user_details(user_id)

        # Assertions
        assertions.assert_status_code(response, 404)
        assertions.assert_response_code(response, 404)
        assertions.assert_error_response(response, 404, "User not found")
        assertions.assert_response_time(response_time, 5.0)

    @allure.story("Get User Details - Negative Cases")
    @allure.title("Get details with negative user ID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_details_negative_id(self, user_api):
        """Test getting details with negative user ID"""
        user_id = -1  # Negative user ID

        response, response_time = user_api.get_user_details(user_id)

        # Assertions
        assertions.assert_status_code(response, 404)
        assertions.assert_response_code(response, 404)
        assertions.assert_error_response(response, 404, "User not found")
        assertions.assert_response_time(response_time, 5.0)


@allure.feature("User Management API")
class TestUpdateUserEmail:
    """Test cases for Update User Email API"""

    @allure.story("Update User Email - Positive Cases")
    @allure.title("Update email with valid data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_user_email_valid(self, user_api):
        """Test updating user email with valid data"""
        user_id = data_generator.get_created_user_ids()[0]
        new_email = data_generator.generate_unique_email()

        response, response_time = user_api.update_user_email(user_id, new_email)

        # Assertions
        assertions.assert_status_code(response, 200)
        assertions.assert_response_code(response, 200)
        assertions.assert_response_message(response, "success")
        assertions.assert_response_time(response_time, 5.0)

    @allure.story("Update User Email - Negative Cases")
    @allure.title("Update email with invalid format")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_user_email_invalid_format(self, user_api):
        """Test updating user email with invalid format"""
        user_id = data_generator.get_created_user_ids()[0]
        invalid_email = "not-an-email"

        response, response_time = user_api.update_user_email(user_id, invalid_email)

        # Assertions
        assertions.assert_status_code(response, 400)
        assertions.assert_response_code(response, 400)
        assertions.assert_error_response(response, 400, "Invalid parameters")
        assertions.assert_response_time(response_time, 5.0)

    @allure.story("Update User Email - Negative Cases")
    @allure.title("Update email for non-existent user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_user_email_nonexistent(self, user_api):
        """Test updating email for non-existent user"""
        user_id = 999  # Non-existent user
        new_email = data_generator.generate_unique_email()

        response, response_time = user_api.update_user_email(user_id, new_email)

        # Assertions
        assertions.assert_status_code(response, 404)
        assertions.assert_response_code(response, 404)
        assertions.assert_error_response(response, 404, "User not found")
        assertions.assert_response_time(response_time, 5.0)

    @allure.story("Update User Email - Negative Cases")
    @allure.title("Update email with empty email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_user_email_empty(self, user_api):
        """Test updating user email with empty email"""
        user_id = 1
        empty_email = ""

        response, response_time = user_api.update_user_email(user_id, empty_email)

        # Assertions
        assertions.assert_status_code(response, 400)
        assertions.assert_response_code(response, 400)
        assertions.assert_error_response(response, 400, "Invalid parameters")
        assertions.assert_response_time(response_time, 5.0)


@allure.feature("User Management API")
class TestDeleteUser:
    """Test cases for Delete User API"""

    @allure.story("Delete User - Positive Cases")
    @allure.title("Delete existing user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_user_existing(self, user_api):
        """Test deleting existing user"""
        user_id = data_generator.get_created_user_ids()[0]

        response, response_time = user_api.delete_user(user_id)

        # Assertions
        assertions.assert_status_code(response, 200)
        assertions.assert_response_code(response, 200)
        assertions.assert_response_message(response, "success")
        assertions.assert_response_time(response_time, 5.0)

    @allure.story("Delete User - Negative Cases")
    @allure.title("Delete non-existent user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user_nonexistent(self, user_api):
        """Test deleting non-existent user"""
        user_id = 999  # Non-existent user

        response, response_time = user_api.delete_user(user_id)

        # Assertions
        assertions.assert_status_code(response, 404)
        assertions.assert_response_code(response, 404)
        assertions.assert_error_response(response, 404, "User not found")
        assertions.assert_response_time(response_time, 5.0)

    @allure.story("Delete User - Negative Cases")
    @allure.title("Delete user with invalid ID format")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user_invalid_id(self, user_api):
        """Test deleting user with invalid ID format"""
        user_id = "invalid_id"

        response, response_time = user_api.delete_user(user_id)

        # Assertions
        assertions.assert_status_code(response, 404)
        assertions.assert_response_code(response, 404)
        assertions.assert_error_response(response, 404, "User not found")
        assertions.assert_response_time(response_time, 5.0)

    @allure.story("Delete User - Negative Cases")
    @allure.title("Delete user with negative ID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user_negative_id(self, user_api):
        """Test deleting user with negative ID"""
        user_id = -1

        response, response_time = user_api.delete_user(user_id)

        # Assertions
        assertions.assert_status_code(response, 404)
        assertions.assert_response_code(response, 404)
        assertions.assert_error_response(response, 404, "User not found")
        assertions.assert_response_time(response_time, 5.0)


@allure.feature("User Management API")
class TestBatchQueryUsers:
    """Test cases for Batch Query Users API"""

    @allure.story("Batch Query Users - Positive Cases")
    @allure.title("Query users with default pagination")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_batch_query_users_default(self, user_api):
        """Test batch query with default pagination"""
        response, response_time = user_api.batch_query_users()

        # Assertions
        assertions.assert_status_code(response, 200)
        assertions.assert_response_code(response, 200)
        assertions.assert_response_message(response, "success")
        assertions.assert_response_time(response_time, 5.0)

        # Verify response structure
        response_data = response.json()
        assert "data" in response_data
        assert "total" in response_data["data"]
        assert "list" in response_data["data"]
        assert isinstance(response_data["data"]["list"], list)

    @allure.story("Batch Query Users - Positive Cases")
    @allure.title("Query users with custom pagination")
    @allure.severity(allure.severity_level.NORMAL)
    def test_batch_query_users_custom_pagination(self, user_api):
        """Test batch query with custom pagination"""
        response, response_time = user_api.batch_query_users(page=2, size=5)

        # Assertions
        assertions.assert_status_code(response, 200)
        assertions.assert_response_code(response, 200)
        assertions.assert_response_message(response, "success")
        assertions.assert_response_time(response_time, 5.0)

    @allure.story("Batch Query Users - Positive Cases")
    @allure.title("Query users with keyword search")
    @allure.severity(allure.severity_level.NORMAL)
    def test_batch_query_users_keyword_search(self, user_api):
        """Test batch query with keyword search"""
        keyword = "test"
        response, response_time = user_api.batch_query_users(keyword=keyword)

        # Assertions
        assertions.assert_status_code(response, 200)
        assertions.assert_response_code(response, 200)
        assertions.assert_response_message(response, "success")
        assertions.assert_response_time(response_time, 5.0)

    @allure.story("Batch Query Users - Negative Cases")
    @allure.title("Query users with invalid page number")
    @allure.severity(allure.severity_level.NORMAL)
    def test_batch_query_users_invalid_page(self, user_api):
        """Test batch query with invalid page number"""
        response, response_time = user_api.batch_query_users(page=-1, size=10)

        # Assertions
        assertions.assert_status_code(response, 400)
        assertions.assert_response_code(response, 400)
        assertions.assert_error_response(response, 400, "Invalid parameters")
        assertions.assert_response_time(response_time, 5.0)

    @allure.story("Batch Query Users - Negative Cases")
    @allure.title("Query users with invalid page size")
    @allure.severity(allure.severity_level.NORMAL)
    def test_batch_query_users_invalid_size(self, user_api):
        """Test batch query with invalid page size"""
        response, response_time = user_api.batch_query_users(page=1, size=0)

        # Assertions
        assertions.assert_status_code(response, 400)
        assertions.assert_response_code(response, 400)
        assertions.assert_error_response(response, 400, "Invalid parameters")
        assertions.assert_response_time(response_time, 5.0)

    @allure.story("Batch Query Users - Negative Cases")
    @allure.title("Query users with oversized page size")
    @allure.severity(allure.severity_level.NORMAL)
    def test_batch_query_users_oversized(self, user_api):
        """Test batch query with oversized page size"""
        response, response_time = user_api.batch_query_users(page=1, size=1000)

        # Assertions
        assertions.assert_status_code(response, 400)
        assertions.assert_response_code(response, 400)
        assertions.assert_error_response(response, 400, "Invalid parameters")
        assertions.assert_response_time(response_time, 5.0)


@allure.feature("User Management API")
class TestAPIIntegration:
    """Comprehensive integration test cases including edge cases, business logic, and performance"""

    @allure.story("User Lifecycle Integration")
    @allure.title("Complete user lifecycle test")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_complete_user_lifecycle(self, user_api):
        """Test complete user lifecycle: create -> get -> update -> delete"""
        # Step 1: Create user
        user_data = data_generator.generate_user_data()
        create_response, create_time = user_api.create_user(user_data)

        assertions.assert_status_code(create_response, 200)
        user_id = create_response.json()["data"]["id"]

        # Step 2: Get user details
        get_response, get_time = user_api.get_user_details(user_id)
        assertions.assert_status_code(get_response, 200)

        # Step 3: Update user email
        new_email = data_generator.generate_unique_email()
        update_response, update_time = user_api.update_user_email(user_id, new_email)
        assertions.assert_status_code(update_response, 200)

        # Step 4: Query users (should include our user)
        query_response, query_time = user_api.batch_query_users()
        assertions.assert_status_code(query_response, 200)

        # Step 5: Delete user
        delete_response, delete_time = user_api.delete_user(user_id)
        assertions.assert_status_code(delete_response, 200)

        # Verify user is deleted
        get_deleted_response, _ = user_api.get_user_details(user_id)
        assertions.assert_status_code(get_deleted_response, 404)

    @allure.story("User Lifecycle")
    @allure.title("Update email for deleted user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_email_deleted_user(self, user_api):
        """Test updating email for a user that has been deleted"""
        # First create a user
        user_data = data_generator.generate_user_data()
        create_response, _ = user_api.create_user(user_data)
        user_id = create_response.json()["data"]["id"]

        # Delete the user
        delete_response, _ = user_api.delete_user(user_id)
        assertions.assert_status_code(delete_response, 200)

        # Try to update email for deleted user
        new_email = data_generator.generate_unique_email()
        response, response_time = user_api.update_user_email(user_id, new_email)

        # Should fail with user not found
        assertions.assert_status_code(response, 404)
        assertions.assert_response_code(response, 404)
        assertions.assert_error_response(response, 404, "User not found")

    @allure.story("User Lifecycle")
    @allure.title("Get details of deleted user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_details_deleted_user(self, user_api):
        """Test getting details of a user that has been deleted"""
        # First create a user
        user_data = data_generator.generate_user_data()
        create_response, _ = user_api.create_user(user_data)
        user_id = create_response.json()["data"]["id"]

        # Delete the user
        delete_response, _ = user_api.delete_user(user_id)
        assertions.assert_status_code(delete_response, 200)

        # Try to get details of deleted user
        response, response_time = user_api.get_user_details(user_id)

        # Should fail with user not found
        assertions.assert_status_code(response, 404)
        assertions.assert_response_code(response, 404)
        assertions.assert_error_response(response, 404, "User not found")

    @allure.story("Data Consistency")
    @allure.title("Create user with duplicate username")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_duplicate_username(self, user_api):
        """Test creating user with username that already exists"""
        # First create a user
        user_data = data_generator.generate_user_data()
        create_response, _ = user_api.create_user(user_data)
        assertions.assert_status_code(create_response, 200)

        # Try to create another user with same username
        duplicate_user_data = data_generator.generate_user_data(
            username=user_data["username"]
        )
        response, response_time = user_api.create_user(duplicate_user_data)

        # Should fail with duplicate username error
        assertions.assert_status_code(response, 409)
        assertions.assert_response_code(response, 409)
        assertions.assert_error_response(response, 409, "Username already exists")

    @allure.story("Data Consistency")
    @allure.title("Create user with duplicate email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_duplicate_email(self, user_api):
        """Test creating user with email that already exists"""
        # First create a user
        user_data = data_generator.generate_user_data()
        create_response, _ = user_api.create_user(user_data)
        assertions.assert_status_code(create_response, 200)

        # Try to create another user with same email
        duplicate_user_data = data_generator.generate_user_data(
            email=user_data["email"]
        )
        response, response_time = user_api.create_user(duplicate_user_data)

        # Should fail with duplicate email error
        assertions.assert_status_code(response, 409)
        assertions.assert_response_code(response, 409)
        assertions.assert_error_response(response, 409, "Email already exists")

    @allure.story("Boundary Values")
    @allure.title("Create user with maximum length username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_max_username_length(self, user_api):
        """Test creating user with maximum allowed username length"""
        max_username = "a" * 50  # Assuming 50 char limit
        user_data = data_generator.generate_user_data(username=max_username)

        response, response_time = user_api.create_user(user_data)

        # Should succeed with max length
        assertions.assert_status_code(response, 200)
        assertions.assert_response_code(response, 200)
        assertions.assert_response_message(response, "success")

    @allure.story("Boundary Values")
    @allure.title("Create user with username exceeding maximum length")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_username_too_long(self, user_api):
        """Test creating user with username exceeding maximum length"""
        too_long_username = "a" * 100  # Exceeds reasonable limit
        user_data = data_generator.generate_user_data(username=too_long_username)

        response, response_time = user_api.create_user(user_data)

        # Should fail with validation error
        assertions.assert_status_code(response, 400)
        assertions.assert_response_code(response, 400)
        assertions.assert_error_response(
            response, 400, "Username exceeds maximum length"
        )

    @allure.story("Special Characters")
    @allure.title("Create user with special characters in username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_special_characters_username(self, user_api):
        """Test creating user with special characters in username"""
        special_username = "user@#$%^&*()_+-=[]{}|;':\",./<>?"
        user_data = data_generator.generate_user_data(username=special_username)

        response, response_time = user_api.create_user(user_data)

        # Should fail with validation error
        assertions.assert_status_code(response, 400)
        assertions.assert_response_code(response, 400)
        assertions.assert_error_response(
            response, 400, "Username contains invalid characters"
        )

    @allure.story("Special Characters")
    @allure.title("Create user with unicode characters")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_unicode_username(self, user_api):
        """Test creating user with unicode characters in username"""
        unicode_username = "用户测试123"
        user_data = data_generator.generate_user_data(username=unicode_username)

        response, response_time = user_api.create_user(user_data)

        # Should fail with validation error (assuming ASCII only)
        assertions.assert_status_code(response, 400)
        assertions.assert_response_code(response, 400)
        assertions.assert_error_response(
            response, 400, "Username contains invalid characters"
        )

    @allure.story("Email Validation")
    @allure.title("Create user with extremely long email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_long_email(self, user_api):
        """Test creating user with extremely long email address"""
        long_email = "a" * 200 + "@" + "b" * 200 + ".com"
        user_data = data_generator.generate_user_data(email=long_email)

        response, response_time = user_api.create_user(user_data)

        # Should fail with validation error
        assertions.assert_status_code(response, 400)
        assertions.assert_response_code(response, 400)
        assertions.assert_error_response(response, 400, "Email address too long")

    @allure.story("Email Validation")
    @allure.title("Create user with multiple @ symbols in email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_multiple_at_symbols(self, user_api):
        """Test creating user with multiple @ symbols in email"""
        invalid_email = "user@@domain.com"
        user_data = data_generator.generate_user_data(email=invalid_email)

        response, response_time = user_api.create_user(user_data)

        # Should fail with validation error
        assertions.assert_status_code(response, 400)
        assertions.assert_response_code(response, 400)
        assertions.assert_error_response(response, 400, "Invalid parameters")

    @allure.story("Password Validation")
    @allure.title("Create user with password containing only spaces")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_password_only_spaces(self, user_api):
        """Test creating user with password containing only spaces"""
        user_data = data_generator.generate_user_data(password="   ")

        response, response_time = user_api.create_user(user_data)

        # Should fail with validation error
        assertions.assert_status_code(response, 400)
        assertions.assert_response_code(response, 400)
        assertions.assert_error_response(response, 400, "Invalid parameters")

    @allure.story("Password Validation")
    @allure.title("Create user with password containing special characters")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_password_special_chars(self, user_api):
        """Test creating user with password containing special characters"""
        special_password = "P@ssw0rd!@#$%^&*()"
        user_data = data_generator.generate_user_data(password=special_password)

        response, response_time = user_api.create_user(user_data)

        # Should succeed with special characters
        assertions.assert_status_code(response, 200)
        assertions.assert_response_code(response, 200)
        assertions.assert_response_message(response, "success")

    @allure.story("Pagination - Boundary Values")
    @allure.title("Query users with page size of 0")
    @allure.severity(allure.severity_level.NORMAL)
    def test_batch_query_page_size_zero(self, user_api):
        """Test batch query with page size of 0"""
        response, response_time = user_api.batch_query_users(page=1, size=0)

        # Should fail with invalid parameters
        assertions.assert_status_code(response, 400)
        assertions.assert_response_code(response, 400)
        assertions.assert_error_response(response, 400, "Invalid parameters")

    @allure.story("Pagination - Boundary Values")
    @allure.title("Query users with negative page number")
    @allure.severity(allure.severity_level.NORMAL)
    def test_batch_query_negative_page(self, user_api):
        """Test batch query with negative page number"""
        response, response_time = user_api.batch_query_users(page=-1, size=10)

        # Should fail with invalid parameters
        assertions.assert_status_code(response, 400)
        assertions.assert_response_code(response, 400)
        assertions.assert_error_response(response, 400, "Invalid parameters")

    @allure.story("Pagination - Boundary Values")
    @allure.title("Query users with page size exceeding maximum")
    @allure.severity(allure.severity_level.NORMAL)
    def test_batch_query_oversized_page(self, user_api):
        """Test batch query with page size exceeding maximum allowed"""
        response, response_time = user_api.batch_query_users(page=1, size=1000)

        # Should fail with invalid parameters
        assertions.assert_status_code(response, 400)
        assertions.assert_response_code(response, 400)
        assertions.assert_error_response(response, 400, "Invalid parameters")

    @allure.story("Pagination - Boundary Values")
    @allure.title("Query users with page number 0")
    @allure.severity(allure.severity_level.NORMAL)
    def test_batch_query_page_zero(self, user_api):
        """Test batch query with page number 0"""
        response, response_time = user_api.batch_query_users(page=0, size=10)

        # Should fail with invalid parameters
        assertions.assert_status_code(response, 400)
        assertions.assert_response_code(response, 400)
        assertions.assert_error_response(response, 400, "Invalid parameters")

    @allure.story("Pagination - Edge Cases")
    @allure.title("Query users with very large page number")
    @allure.severity(allure.severity_level.NORMAL)
    def test_batch_query_large_page_number(self, user_api):
        """Test batch query with very large page number"""
        response, response_time = user_api.batch_query_users(page=999999, size=10)

        # Should succeed but return empty results
        assertions.assert_status_code(response, 200)
        assertions.assert_response_code(response, 200)
        assertions.assert_response_message(response, "success")

        # Verify results structure (may have some data due to mock implementation)
        response_data = response.json()
        assert "data" in response_data
        assert "list" in response_data["data"]
        assert isinstance(response_data["data"]["list"], list)

    @allure.story("Pagination - Edge Cases")
    @allure.title("Query users with keyword containing special characters")
    @allure.severity(allure.severity_level.NORMAL)
    def test_batch_query_special_characters_keyword(self, user_api):
        """Test batch query with keyword containing special characters"""
        special_keyword = "test@#$%^&*()_+-=[]{}|;':\",./<>?"
        response, response_time = user_api.batch_query_users(keyword=special_keyword)

        # Should succeed (keyword filtering should handle special chars)
        assertions.assert_status_code(response, 200)
        assertions.assert_response_code(response, 200)
        assertions.assert_response_message(response, "success")

    @allure.story("Pagination - Edge Cases")
    @allure.title("Query users with very long keyword")
    @allure.severity(allure.severity_level.NORMAL)
    def test_batch_query_long_keyword(self, user_api):
        """Test batch query with very long keyword"""
        long_keyword = "a" * 1000  # Very long keyword
        response, response_time = user_api.batch_query_users(keyword=long_keyword)

        # Should succeed but likely return empty results
        assertions.assert_status_code(response, 200)
        assertions.assert_response_code(response, 200)
        assertions.assert_response_message(response, "success")

    @allure.story("Performance Testing")
    @allure.title("API response time validation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_api_response_times(self, user_api):
        """Test that all APIs respond within acceptable time limits"""
        # Test create user response time
        user_data = data_generator.generate_user_data()
        _, create_time = user_api.create_user(user_data)
        assertions.assert_response_time(create_time, 2.0)

        # Test get user response time
        _, get_time = user_api.get_user_details(1)
        assertions.assert_response_time(get_time, 2.0)

        # Test update user response time
        _, update_time = user_api.update_user_email(
            1, data_generator.generate_unique_email()
        )
        assertions.assert_response_time(update_time, 2.0)

        # Test batch query response time
        _, query_time = user_api.batch_query_users()
        assertions.assert_response_time(query_time, 2.0)

        # Test delete user response time
        _, delete_time = user_api.delete_user(1)
        assertions.assert_response_time(delete_time, 2.0)

    @allure.story("Performance - Response Time")
    @allure.title("Batch query with large page size")
    @allure.severity(allure.severity_level.NORMAL)
    def test_batch_query_large_page_size(self, user_api):
        """Test batch query with large but valid page size"""
        response, response_time = user_api.batch_query_users(page=1, size=100)

        # Should succeed within reasonable time
        assertions.assert_status_code(response, 200)
        assertions.assert_response_time(response_time, 5.0)
