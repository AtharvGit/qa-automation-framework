import pytest
import time
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

@pytest.mark.cart
class TestCart:
    
    @pytest.fixture(autouse=True)
    def login_first(self, driver):
        driver.delete_all_cookies()
        driver.refresh()
        
        login_page = LoginPage(driver)
        login_page.login('standard_user', 'secret_sauce')
        yield

    def test_add_single_item_to_cart(self, driver):
        inventory_page = InventoryPage(driver)

        item_to_add = 'Sauce Labs Backpack'
        
        # 1. Add item
        inventory_page.add_item_to_cart(item_to_add)
        
        # 2. Wait a split second for the animation/popup to clear
        # This is crucial for stability on local Windows runs
        time.sleep(1) 
        
        # 3. Go to cart
        inventory_page.click_shopping_cart()

        # 4. Verify
        cart_page = CartPage(driver)
        
        # Ensure we actually got to the cart page
        assert cart_page.is_on_cart_page(), "Did not navigate to cart page!"
        assert cart_page.is_item_in_cart(item_to_add), "Item was not found in cart!"