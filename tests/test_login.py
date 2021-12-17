from pages.LoginPage import LoginPage
from tests.test_base import BaseTest


class TestLogin(BaseTest):

    def test_login(self):
        assert 'Digital Bank' == self.driver.title
