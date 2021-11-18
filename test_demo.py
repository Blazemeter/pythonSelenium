from selenium import webdriver
import pytest
from selenium.webdriver.common.by import By


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.close()
    driver.quit()


def test_verify_title(driver):
    driver.get("http://dbankdemo.com/bank/login")
    assert 'Digital Bank' == driver.title


def test_login(driver):
    # find username element input and type jsmith@demo.io
    driver.find_element(By.ID, 'username').send_keys('jsmith@demo.io')
    # find password element input and type Demo123!
    driver.find_element(By.ID, 'password').send_keys('Demo123!')
    # click sign in button
    driver.find_element(By.ID, 'submit').click()

    assert 'home' in driver.current_url
