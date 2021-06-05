import os
import pytest
import shutil
import allure
from _pytest.fixtures import Parser, FixtureRequest
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome


def pytest_addoption(parser: Parser) -> None:
    parser.addoption('--timeout_limit', default=10.0)


def pytest_configure(config):
    abs_path = os.path.abspath(os.curdir)

    base_test_dir = os.path.join(abs_path, "tmp", "tests")

    if not hasattr(config, 'workerinput'):
        if os.path.exists(base_test_dir):
            shutil.rmtree(base_test_dir)
        os.makedirs(base_test_dir)

    config.abs_path = abs_path
    config.base_test_dir = base_test_dir


@pytest.fixture(scope="session")
def configuration(request: FixtureRequest) -> dict:
    return {
        'timeout_limit': request.config.getoption('timeout_limit')
    }


@pytest.fixture(scope="function")
def driver():
    manager = ChromeDriverManager(version='latest', log_level=0)
    driver = Chrome(executable_path=manager.install())
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def test_dir(request: FixtureRequest) -> str:
    test_name = request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_')
    test_dir = os.path.join(request.config.base_test_dir, test_name)
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope="function", autouse=True)
def ui_report(driver: webdriver.Chrome, request: FixtureRequest, test_dir: str) -> None:
    failed = request.session.testsfailed
    yield
    if request.session.testsfailed > failed:
        screenshot_file = os.path.join(test_dir, 'failure.png')
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'failure.png', attachment_type=allure.attachment_type.PNG)

        browser_logfile = os.path.join(test_dir, 'browser.log')
        with open(browser_logfile, 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")

        with open(browser_logfile, 'r') as f:
            allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)
