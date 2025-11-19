import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage 

@pytest.mark.login
class TestLoginPage:

    def test_login_page_elements_are_visible(self, driver):
        """
        Test case to verify that the login page loads and elements are visible.
        """
        login_page = LoginPage(driver)
        
        # FIX: We must explicitly load the page first!
        login_page.load_page()
        
        # Verify title and elements
        assert login_page.get_page_title("Swag Labs")
        assert login_page.is_element_visible(login_page.USERNAME_INPUT)
        assert login_page.is_element_visible(login_page.PASSWORD_INPUT)
        assert login_page.is_element_visible(login_page.LOGIN_BUTTON)


    def test_successful_login(self, driver):
        """
        Test case to verify a valid login.
        """
        login_page = LoginPage(driver)
        login_page.login("standard_user", "secret_sauce")
        
        # Verify we moved to the inventory page
        inventory_page = InventoryPage(driver)
        assert inventory_page.is_page_title_visible(), "Inventory page title was not visible"


    def test_locked_out_user_login(self, driver):
        """
        Test case to verify error message for a locked-out user.
        """
        # FIX: Clear cookies and refresh to ensure we are logged out from previous tests
        # This prevents the browser from remembering the successful login from the previous test
        driver.delete_all_cookies()
        driver.refresh()
        
        login_page = LoginPage(driver)
        login_page.login("locked_out_user", "secret_sauce")

        # Verify we are NOT on the inventory page
        assert "inventory.html" not in login_page.get_current_url()
        
        # Verify the specific error message
        expected_error = "Epic sadface: Sorry, this user has been locked out."
        assert login_page.get_error_message() == expected_error