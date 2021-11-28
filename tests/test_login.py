from pages.LoginPage import LoginPage
from tests.test_base import BaseTest


class TestLogin(BaseTest):

    def test_login(self, base_url, username, password):
        self.loginPage = LoginPage(self.driver)

        assert 'Digital Bank' == self.driver.title
