from pages.HomePage import HomePage
from tests.test_base import BaseTest


class TestHomePage(BaseTest):

    def test_verify_version(self):
        self.homepage = HomePage(self.driver)

        assert '2.1.0.7' in self.homepage.get_version()
