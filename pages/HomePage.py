from selenium.webdriver.common.by import By

from pages.BasePage import BasePage


class HomePageLocators:
    version_button = (By.ID, 'aboutLink')
    version_modal = (By.CLASS_NAME, 'modal-body')


class HomePage(BasePage):
    # -- HomePage constructor -- #
    def __init__(self, driver):
        super().__init__(driver)

    # -- Page actions -- #
    def get_version(self):
        self.click_element(HomePageLocators.version_button)
        return self.get_element_text(HomePageLocators.version_modal)
