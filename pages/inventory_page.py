from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class InventoryPage(BasePage):
    
    # --- Locators ---
    PAGE_TITLE = (By.CSS_SELECTOR, ".title")
    SHOPPING_CART_ICON = (By.ID, "shopping_cart_container")
    
    # FIX: A robust XPath that finds the Item Name, goes up to the Card, then finds the Button.
    ADD_TO_CART_BUTTON = (By.XPATH, "//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button")

    def __init__(self, driver):
        super().__init__(driver)

    # --- Verifications ---
    def is_page_title_visible(self):
        return self.is_element_visible(self.PAGE_TITLE)

    def is_cart_icon_visible(self):
        return self.is_element_visible(self.SHOPPING_CART_ICON)

    # --- Actions ---
    def add_item_to_cart(self, item_name):
        """
        Adds a specific item to the cart by its name.
        """
        # Dynamic locator strategy
        item_locator = (self.ADD_TO_CART_BUTTON[0], self.ADD_TO_CART_BUTTON[1].format(item_name=item_name))
        self.do_click(item_locator)

    def click_shopping_cart(self):
        self.do_click(self.SHOPPING_CART_ICON)