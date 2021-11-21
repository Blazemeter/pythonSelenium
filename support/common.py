from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_element(driver, by_locator):
    return WebDriverWait(driver, 10).until(EC.visibility_of_element_located(by_locator))


def get_element_text(driver, by_locator):
    return get_element(driver, by_locator).text


def type_element(driver, by_locator, text):
    get_element(driver, by_locator).send_keys(text)


def click_element(driver, by_locator):
    get_element(driver, by_locator).click()


def is_element_visible(driver, by_locator):
    get_element(driver, by_locator).is_displayed()

