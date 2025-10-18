# User Management API Testing Framework

A comprehensive automated testing framework for User Management RESTful APIs, built with Python, pytest, and Allure reporting.

## Features

- **Complete API Coverage**: Tests 5 User Management API endpoints
- **Mock-Based Testing**: Uses JSON test data
- **Multi-Environment Support**: Easy switching between test/staging/production
- **Reporting**: Allure reports with request/response details
- **Dynamic Test Data**: Auto-generated unique test data with cleanup
- **Error Handling**: Retry mechanisms and error validation

## API Coverage

| API Endpoint | Method | Status |
|-------------|--------|------------|--------|
| Create User | POST | Covered |
| Get User Details | GET | Covered |
| Update User Email | PUT | Covered |
| Delete User | DELETE | Covered |
| Batch Query Users | GET | Covered |
| **Integration Tests** | - | Covered |


## Prerequisites

- **Python 3.8+**
- **pip** 
- **Allure** (for report generation)
- **Git** (for cloning the repository)

## Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd novum_studio
```

2. **Create virtual environment (recommended):**
```bash
python -m venv novam_venv
source novam_venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Verify installation:**
```bash
pytest --version
allure --version
```

### Key Dependencies
- **pytest**: Test framework with advanced features
- **allure-pytest**: Allure reporting integration
- **requests**: HTTP client for API testing
- **faker**: Dynamic test data generation

## Quick Start

### Run All Tests
```bash
# Run all API tests with Allure reporting
export TEST_ENV=test
pytest testcases/ --alluredir=reports

# View reports
allure serve reports
```

### Run Specific Test
```bash
pytest testcases/test_user_management.py::TestCreateUser::test_create_user_normal --alluredir=reports
```

### Environment Switching
```bash
# Test environment (default, uses mocking)
export TEST_ENV=test
pytest testcases/ --alluredir=reports

# Staging environment
export TEST_ENV=staging
pytest testcases/ --alluredir=reports

# Production environment
export TEST_ENV=production
pytest testcases/ --alluredir=reports
```

### Configuration Files
- `config/test_config.py` - Environment-specific settings
- `data/test_users.json` - Test data and mock responses
- `data/api_responses.json` - Expected response templates

## Project Structure

```
novum_studio/
├── api/                          # API layer components
│   ├── __init__.py
│   ├── base_api.py              # Base API client mocking
│   └── user_api.py              # User Management API endpoints
├── common/                       # Shared utilities and helpers
│   ├── __init__.py
│   ├── data_generator.py        # Dynamic test data generation with Faker
│   ├── assertions.py            # Custom assertion helpers for API testing
│   └── logger.py                # Structured logging with configurable levels
├── testcases/                    # Test case implementations
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures and Allure integration
│   └── test_user_management.py  # tests 
├── config/                       # Configuration management
│   └── test_config.py           # Multi-environment configuration
├── data/                        # Test data and mock responses
│   ├── test_users.json          # Initial user test data
│   └── api_responses.json      # Mock response templates
├── reports/                     # Test reports and artifacts
│   ├── *.json                   # Allure test results
│   └── environment.properties  # Environment configuration
├── requirements.txt              # Python dependencies
├── .gitignore                   # Git ignore rules
└── README.md                    # Project documentation
```

## Test Data Management

### Dynamic Data Generation
- **Unique Usernames**: Auto-generated with Faker
- **Unique Emails**: Auto-generated with Faker
- **Password Generation**: Secure password generation with length validation
- **Test Data Cleanup**: Automatic cleanup after test execution
- **Data Isolation**: Each test uses independent data

### Mock Data Configuration
- **Test Data**: `data/test_users.json` - Sample users
- **Expected Responses**: `data/api_responses.json` - Response templates

### Retry Mechanisms
- **Configurable Retries**: Environment-specific retry attempts
- **Exponential Backoff**: Intelligent retry delays
- **Error Handling**: Comprehensive error logging and recovery
- **Timeout Management**: Configurable request timeouts

## Extending the Framework

### Adding New APIs
1. **Create API Client**: 
   - Extend `BaseAPI` class in `api/` directory
   - Implement endpoint-specific methods
   - Add proper error handling and logging

2. **Add Test Cases**: 
   - Create test class in `testcases/` directory
   - Use existing assertion helpers
   - Follow Allure reporting patterns

3. **Update Mock Data**: 
   - Add mock responses to `data/api_responses.json`
   - Update validation logic in `BaseAPI._get_mock_response()`
   - Add test data to `data/test_users.json` if needed

4. **Configure Environment**:
   - Update `config/test_config.py` for new endpoints
   - Add environment-specific settings
