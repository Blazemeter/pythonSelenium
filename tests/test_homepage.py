from pages.HomePage import HomePage
from tests.test_base import BaseTest


class TestHomePage(BaseTest):

    def test_verify_version_passed(self):
        self.homepage = HomePage(self.driver)

        assert '2.1.0.7' in self.homepage.get_version()

    # [Commented out] - For Blazemeter report demo purpose
    # def test_verify_version_failed(self):
    #     self.homepage = HomePage(self.driver)
    #
    #     assert 'some wrong value' in self.homepage.get_version()
