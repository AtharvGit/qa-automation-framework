import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--remote", action="store_true", default=False)

@pytest.fixture(scope="module")
def driver(request):
    browser = request.config.getoption("--browser")
    is_remote = request.config.getoption("--remote")
    
    print(f'\n[setup] Starting {browser} (Remote: {is_remote})...')
    
    if is_remote:
        # --- REMOTE EXECUTION (DOCKER GRID) ---
        # Connects to the Selenium Hub container
        hub_url = "http://selenium-hub:4444/wd/hub"
        
        if browser == "chrome":
            options = ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            # We can add incognito here too just to be safe
            options.add_argument("--incognito")
        elif browser == "firefox":
            options = FirefoxOptions()
            options.add_argument("--incognito")
        
        try:
            driver = webdriver.Remote(command_executor=hub_url, options=options)
        except Exception as e:
            pytest.fail(f"Could not connect to Selenium Grid at {hub_url}. Error: {e}")

    else:
        # --- LOCAL EXECUTION (YOUR LAPTOP) ---
        # This keeps your "Nuclear" fix for local debugging
        if browser == "chrome":
            service = ChromeService(ChromeDriverManager().install())
            options = ChromeOptions()
            
            # NUCLEAR OPTION to stop popups locally
            options.add_argument("--incognito")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-save-password-bubble")
            options.add_argument("--password-store=basic")
            options.add_argument("--disable-features=PasswordLeakDetection,PasswordManager,SavePassword,AutofillAddressEnabled,AutofillCreditCardEnabled")
            
            prefs = {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.default_content_setting_values.notifications": 2
            }
            options.add_experimental_option("prefs", prefs)
            
            driver = webdriver.Chrome(service=service, options=options)
        else:
            raise ValueError("Only Chrome is supported for local testing currently")

    driver.implicitly_wait(10)
    yield driver
    
    print('\n[teardown] quitting browser')
    driver.quit()