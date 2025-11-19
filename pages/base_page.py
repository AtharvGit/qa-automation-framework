from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def do_click(self, by_locator):
        try:
            self.wait.until(EC.element_to_be_clickable(by_locator)).click()
        except TimeoutException:
            print(f"Error: Element {by_locator} was not clickable after 10 seconds")
            raise
        except NoSuchElementException:
            print(f"Error: Element {by_locator} was not found on the page")
            raise

    def do_send_keys(self, by_locator, text):
        try:
            element = self.wait.until(EC.visibility_of_element_located(by_locator))
            element.clear()
            element.send_keys(text)
        except TimeoutException:
            print(f"Error: Element {by_locator} was not visible after 10 seconds")
            raise
    
    def get_element_text(self, by_locator):
        try:
            element = self.wait.until(EC.visibility_of_element_located(by_locator))
            return element.text
        except TimeoutException:
            print(f"Error: Element {by_locator} was not visible after 10 seconds")
            raise

    def is_element_visible(self, by_locator):
        try:
            self.wait.until(EC.visibility_of_element_located(by_locator))
            return True
        except TimeoutException:
            return False
        
    def get_page_title(self, expected_title):
        try:
            self.wait.until(EC.title_is(expected_title))
            return True
        except TimeoutException:
            print(f"Error: Page title was not '{expected_title}' after 10 seconds")
            return False
        
    def get_current_url(self):
        return self.driver.current_url