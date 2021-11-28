import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="class")
def base_url():
    return os.environ.get('BASE_URL')


@pytest.fixture(scope="class")
def username():
    return os.environ.get('USERNAME')


@pytest.fixture(scope="class")
def password():
    return os.environ.get('PASSWORD')


@pytest.fixture(scope="class")
def driver(request):
    # -- Run configuration - Running the tests under chrome -- #
    s = Service('./drivers/chromedriver')
    driver = webdriver.Chrome(service=s)

    # -- Run configuration - Prepare the browser prior to browser initiation -- #
    driver.maximize_window()

    # -- Run hooks - Set driver on startup -- #
    request.cls.driver = driver

    # -- Teardown method - Final steps -- #
    yield
    driver.close()
    driver.quit()
