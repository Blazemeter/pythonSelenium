from config.config import TestConfig
from pages.BasePage import BasePage
from selenium.webdriver.common.by import By


# -- Login Page Locators -- #
class LoginPageLocators:
    username_input = (By.ID, "username")
    password_input = (By.ID, "password")
    submit_button = (By.ID, "submit")


class LoginPage(BasePage):

    # -- Constructor of the page class -- #
    def __init__(self, driver):
        super().__init__(driver)

    # -- Page actions -- #
    def login(self):
        self.driver.get("{}/login".format(TestConfig.base_url))
        self.type_element(LoginPageLocators.username_input, TestConfig.username)
        self.type_element(LoginPageLocators.password_input, TestConfig.password)
        self.click_element(LoginPageLocators.submit_button)
