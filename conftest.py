import os
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from datetime import datetime

BUILD_ID = int(time.time())


@pytest.fixture(scope="class", params=["chrome", "edge"])
def driver(request):
    # -- Get the browser name from request params -- #
    browser = request.param

    # -- Run configuration - Running the tests local/remote -- #
    if os.getenv('IS_LOCAL') == 'True':

        if browser == 'chrome':
            s = Service('./drivers/chromedriver')
            driver = webdriver.Chrome(service=s)

        if browser == 'edge':
            s = Service('./drivers/msedgedriver')
            driver = webdriver.Edge(service=s)
    else:

        # -- Blazemeter access configuration -- #
        api_key = os.environ.get('API_KEY')
        api_secret = os.environ.get('API_SECRET')
        base = 'a.blazemeter.com'

        # -- BlazeGrid capabilities -- #
        # -- https://a.blazemeter.com/api/v4/grid/capabilities -- #
        # -- https://tinyurl.com/desired-cap-blazemeter) -- #
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        if browser == 'edge':
            browser = 'MicrosoftEdge'  # to support BlazeMeter's grid browsers names
        desired_capabilities = {
            'browserName': browser,
            'blazemeter.buildId': BUILD_ID,
            'blazemeter.testName': 'Selenium course test',
            'blazemeter.reportName': '{report_name}_{timestamp}_{browser}'.format(report_name=request.node.name,
                                                                                  timestamp=now, browser=browser)
        }
        blazegrid_url = 'https://{api_key}:{api_secret}@{base}/api/v4/grid/wd/hub'.format(api_key=api_key,
                                                                                          api_secret=api_secret,
                                                                                          base=base)
        driver = webdriver.Remote(command_executor=blazegrid_url,
                                  desired_capabilities=desired_capabilities)

    # -- Run configuration - Prepare the browser prior to browser initiation -- #
    driver.maximize_window()

    # -- Run hooks - Set driver on startup -- #
    request.cls.driver = driver

    # -- Teardown method - Final steps -- #
    yield driver

    # -- WebDriver browser shutdown -- #
    driver.quit()


# -- Blazemeter report integration -- #
# -- https://tinyurl.com/gui-test-report-blazemeter -- #
@pytest.mark.usefixtures("driver")
@pytest.fixture(scope="function", autouse=True)
def name_blazemeter_reporter(request, driver):
    args = {
        'testCaseName': request.node.name,
        'testSuiteName': request.node.parent.parent.name
    }
    # -- BlazeMeter report start command -- #
    driver.execute_script("/* FLOW_MARKER test-case-start */", args)

    yield

    # -- Check for failed tests and update the report status accordingly -- #
    if request.node.rep_setup.failed:
        message = request.node.rep_setup.longrepr.reprcrash.message
        status = 'broken'
    elif request.node.rep_call.failed:
        message = request.node.rep_call.longrepr.reprcrash.message
        is_assertion = 'AssertionError' in request.node.rep_call.longreprtext
        status = 'failed' if is_assertion else 'broken'
    else:
        message = ''
        status = 'passed'
    args = {
        'status': status,
        'message': message
    }
    # -- BlazeMeter report stop command -- #
    driver.execute_script("/* FLOW_MARKER test-case-stop */", args)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
