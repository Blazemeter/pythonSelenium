from selenium import webdriver
import pytest
from selenium.webdriver.common.by import By

from support.common import get_element, get_element_text, type_element, click_element


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.close()
    driver.quit()


def test_login(driver):
    driver.get("http://dbankdemo.com/bank/login")
    assert 'Digital Bank' == driver.title

    type_element(driver, (By.ID, 'username'), 'jsmith@demo.io')
    type_element(driver, (By.ID, 'password'), 'Demo123!')
    click_element(driver, (By.ID, 'submit'))

    assert 'home' in driver.current_url


def test_verify_version(driver):
    get_element(driver, (By.ID, 'aboutLink')).click()

    assert '2.1.0.7' in get_element_text(driver, (By.CLASS_NAME, 'modal-body'))
