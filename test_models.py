import pytest
from your_flask_app import Seller, Buyer, seller_login, buyer_login

# Test function to verify seller login
@pytest.mark.parametrize("email, password, expected_result", [
    ("valid_email@example.com", "valid_password", "Login successful"),
    ("invalid_email@example.com", "valid_password", "Invalid email or password"),
    ("valid_email@example.com", "invalid_password", "Invalid email or password")
])
def test_seller_login(email, password, expected_result):
    # Create a new instance of the Seller model with the specified email and password
    seller = Seller(email=email, password=password)
    
    # Perform seller login using the seller_login function
    login_result = seller_login(seller)
    
    # Assert the expected result
    assert login_result == expected_result

# Test function to verify buyer login
@pytest.mark.parametrize("email, password, expected_result", [
    ("valid_email@example.com", "valid_password", "Login successful"),
    ("invalid_email@example.com", "valid_password", "Invalid email or password"),
    ("valid_email@example.com", "invalid_password", "Invalid email or password")
])
def test_buyer_login(email, password, expected_result):
    # Create a new instance of the Buyer model with the specified email and password
    buyer = Buyer(email=email, password=password)
    
    # Perform buyer login using the buyer_login function
    login_result = buyer_login(buyer)
    
    # Assert the expected result
    assert login_result == expected_result
