from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    # --- Locators ---
    ITEM_IN_CART = (By.XPATH, "//div[@class='inventory_item_name' and text()='{item_name}']")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def __init__(self, driver):
        super().__init__(driver)

    # --- Verifications ---
    def is_on_cart_page(self):
        """
        Checks if the URL contains 'cart.html'.
        """
        # We check the URL to ensure navigation happened
        return "cart.html" in self.get_current_url()

    def is_item_in_cart(self, item_name):
        """
        Checks if the item is visible in the cart.
        """
        # First, verify we are on the correct page
        if not self.is_on_cart_page():
            print("Error: Not on cart page!")
            return False
            
        item_locator = (self.ITEM_IN_CART[0], self.ITEM_IN_CART[1].format(item_name=item_name))
        return self.is_element_visible(item_locator)