import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from datetime import datetime


@pytest.fixture(scope="class")
def base_url():
    return os.environ.get('BASE_URL')


@pytest.fixture(scope="class")
def username():
    return os.environ.get('USERNAME')


@pytest.fixture(scope="class")
def password():
    return os.environ.get('PASSWORD')


@pytest.fixture(scope="class")
def driver(request):

    # -- Run configuration - Running the tests under chrome local/remote -- #
    if os.getenv('IS_LOCAL') is True:
        s = Service('./drivers/chromedriver')
        driver = webdriver.Chrome(service=s)

    else:

        # -- Blazemeter access configuration -- #
        api_key = os.environ.get('API_KEY')
        api_secret = os.environ.get('API_SECRET')
        base = 'a.blazemeter.com'

        # -- BlazeGrid capabilities -- #
        # -- https://a.blazemeter.com/api/v4/grid/capabilities -- #
        # -- https://tinyurl.com/desired-cap-blazemeter) -- #
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        desired_capabilities = {
            'browserName': 'chrome',
            'blazemeter.reportName': '{report_name}_{timestamp}'.format(report_name=request.node.name,
                                                                        timestamp=now)
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
    yield

    # -- WebDriver browser shutdown -- #
    driver.close()
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
    # -- BlazeMeter report start -- #
    driver.execute_script("/* FLOW_MARKER test-case-start */", args)

    yield

    # -- Check for failed tests and update the report status accordingly -- #
    if request.node.session.testsfailed > 0:
        status = 'failed'
    else:
        status = 'passed'
    args = {
        'status': status,
        'message': '{testCase} {status}'.format(testCase=request.node.session.items[0].originalname,
                                                status=status)
    }
    # -- BlazeMeter report stop -- #
    driver.execute_script("/* FLOW_MARKER test-case-stop */", args)
