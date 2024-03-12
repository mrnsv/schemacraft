import json
import pytest
from requests import post  # Assuming requests library for API calls

# Define various valid JSON data structures for testing
valid_json_data = [
    {
        "name": "John Doe",
        "age": 30,
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "state": "CA"
        },
        "interests": ["programming", "music", "travel"]
    },
    {
        "numbers": [1, 2.5, 33],
        "is_active": True,
        "details": None
    }
]

invalid_json_data = [
    "",  # Empty data
    "{invalid_key: 'value'}",  # Malformed JSON
]


def test_schema_generation_valid_data():
    """Tests generating JSON Schemas from various valid JSON data structures"""

    url = "http://127.0.0.1:5000/"  # Replace with your application URL
    headers = {"Content-Type": "application/json"}

    for data in valid_json_data:
        # Option 1: Using requests library (external API call)
        response = post(url, json=data, headers=headers)
        
        print("Response : ", response)
        print("Data : ", data)
        print("Status Code : ", response.status_code)
        
        assert response.status_code == 200
        response_data = json.loads(response.text)

        # Basic assertions on the generated schema (you can add more)
        assert "type" in response_data
        assert response_data["type"] == "object"
        assert "properties" in response_data

        # Option 2: Using Flask-Client for integrated testing (if installed)
        # from flask_testing import Client
        # with app.test_client() as client:
        #     response = client.post('/', json=data, content_type='application/json')
        #     assert response.status_code == 200
        #     response_data = response.get_json()
        #     # Assertions on the generated schema

def test_schema_generation_invalid_data():
    """Tests error handling for invalid JSON data"""

    url = "http://127.0.0.1:5000/"  # Replace with your application URL
    headers = {"Content-Type": "application/json"}

    for data in invalid_json_data:
        response = post(url, json=data, headers=headers)
        assert response.status_code == 400  # Assert bad request code
        assert "error" in json.loads(response.text)  # Check for error message

# Additional test cases can be added here for different functionalities
