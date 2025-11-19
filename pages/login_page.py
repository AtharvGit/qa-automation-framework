from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    # --- Locators ---
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE_CONTAINER = (By.CSS_SELECTOR, "h3[data-test='error']")

    LOGIN_URL = 'https://www.saucedemo.com/'

    def __init__(self, driver):
        super().__init__(driver)
    
    # --- Actions ---
    def load_page(self):
        """
        Navigates the browser to the login page URL.
        """
        self.driver.get(self.LOGIN_URL)

    def enter_username(self, username):
        self.do_send_keys(self.USERNAME_INPUT, username)  

    def enter_password(self, password):
        self.do_send_keys(self.PASSWORD_INPUT, password)
    
    def click_login(self):
        self.do_click(self.LOGIN_BUTTON)

    def login(self, username, password):
        """
        Helper method to perform the entire login flow.
        """
        self.load_page()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    # --- Verifications ---
    def get_error_message(self):
        return self.get_element_text(self.ERROR_MESSAGE_CONTAINER)
    
    def is_login_button_displayed(self):
        return self.is_element_visible(self.LOGIN_BUTTON)