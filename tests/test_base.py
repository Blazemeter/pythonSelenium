import pytest

from pages.LoginPage import LoginPage


@pytest.mark.usefixtures("driver")
class BaseTest:
    # -- Setup method - occurs before each test case within the class -- #
    def setup_method(self):
        self.loginPage = LoginPage(self.driver)
        self.loginPage.login()

    # -- Teardown method - occurs after each test case within the class-- #
    def teardown_method(self):
        print("test teardown")
