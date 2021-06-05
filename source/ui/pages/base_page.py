from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ActionChains, Chrome
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import exceptions

from utils.decorators import wait


class BasePageActions(object):
    url = None
    locators = None

    def __init__(self, driver: Chrome, configuration: dict) -> None:
        """
        Инициализация базового класса для работы с элементами на странице.
        :param driver: драйвер Google Chrome.
        :param configuration: конфигурация тестирования.
        """
        self.driver = driver
        self.configuration = configuration

        self.driver.get(url=self.url)

    def click(self, locator: tuple) -> None:
        """
        Нажать на элемент на странице.
        :param locator: локатор элемента.
        :return: None.
        """
        def _click():
            self.action_chains.click(on_element=self.find_element(locator=locator)).perform()
            return

        return wait(
            _method=_click,
            _error=exceptions.StaleElementReferenceException,
            _timeout=self.configuration['timeout_limit']
        )

    def send_keys(self, locator: tuple = None, send_data: str = "", auto_clear: bool = True) -> None:
        """
        Отправить данные через ActionChains.send_keys.
        :param locator: локатор элемента.
        :param send_data: отправляемые данные.
        :param auto_clear: автоматическая очистка элемента перед отправкой. По умолчанию: True.
        :return: None
        """
        def _send_keys():
            element = self.find_element(locator=locator)
            if auto_clear:
                element.clear()
            self.action_chains.send_keys_to_element(element, send_data).perform()

        return wait(
            _method=_send_keys,
            _error=exceptions.TimeoutException,
            _timeout=self.configuration['timeout_limit']
        )

    def wait(self, timeout: float = None) -> WebDriverWait:
        """
        Настройка ожиданий.
        :param timeout: время ожидания. По умолчанию: None.
        :return: WebDriverWait.
        """
        if timeout is None:
            timeout = self.configuration['timeout_limit']
        return WebDriverWait(self.driver, timeout=timeout)

    def find_element(self, locator: tuple, timeout: float = None) -> WebElement:
        """
        Найти элемент на странице.
        :param locator: локатор элемента.
        :param timeout: время для нахождения элемента.
        :return: WebElement
        """
        return self.wait(timeout=timeout).until(ec.presence_of_element_located(locator=locator))

    def get_text_from_element(self, locator: tuple, timeout: float = None) -> str:
        """
        Получение текста из элемента страницы.
        :param locator: локатор элемента.
        :param timeout: время для нахождения элемента.
        :return: str
        """
        return wait(
            _method=lambda: self.find_element(locator=locator, timeout=timeout).text,
            _error=exceptions.StaleElementReferenceException,
            _timeout=self.configuration['timeout_limit']
        )

    def get_attr_from_element(self, attribute_name: str, locator: tuple, timeout: float = None) -> str:
        """
            Получение атрибута из элемента.
            :param attribute_name: название атрибута.
            :param locator: локатор элемента.
            :param timeout: время для нахождения элемента.
            :return: str
        """
        def _get():
            return self.find_element(locator=locator, timeout=timeout).get_attribute(attribute_name)

        return wait(
            _method=_get,
            _error=exceptions.StaleElementReferenceException,
            _timeout=self.configuration['timeout_limit']
        )

    @property
    def action_chains(self) -> ActionChains:
        """
        Вернуть объект Action Chains в Selenium.
        :return: ActionChains property.
        """
        return ActionChains(self.driver)
