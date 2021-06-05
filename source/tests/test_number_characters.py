import re
import pytest
import allure
from selenium.webdriver.remote.webdriver import WebDriver

from ui.pages.main_page import MainPage


class BaseTest(object):
    driver: WebDriver = None
    main_page: MainPage = None

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, driver, configuration):
        self.driver = driver
        self.main_page = MainPage(driver=driver, configuration=configuration)

    @staticmethod
    def do_asserts(arr: list) -> None:
        errors = []
        for e in arr:
            try:
                with allure.step(f'{e[2]} (Try to assert "{e[0]}" and "{e[1]}")'):
                    assert e[0] == e[1], f"Not equal: '{e[0]}' != '{e[1]}'"
            except AssertionError as e:
                errors.append(e.args[0])

        if errors:
            raise AssertionError('\n'.join(errors))


class TestCasePositive(BaseTest):

    result: dict = None

    def prepare(self, text: str) -> None:
        # Выполняем позитивный тест.
        self.main_page.exec_query(text=text)

        # Получаем результат
        self.result = self.main_page.get_results()

    @pytest.mark.UI
    @pytest.mark.SMOKE
    @pytest.mark.parametrize("text", ["Text for example"], ids=["Positive text"])
    def test_number_characters_positive(self, text: str) -> None:
        self.prepare(text=text)

        # Выполняем проверки данных.
        self.do_asserts([(self.result['count_symbols'], len(text), "Количество символов"),
                         (self.result['count_symbols_without_spaces'], len(''.join(text.split(' '))), "Количество символов без пробелов"),
                         (self.result['count_words'], len(text.split(' ')), "Количество слов"),
                         (self.result['count_of_commas'], text.count(','), "Количество запятых"),
                         (self.result['count_of_dots'], text.count('.'), "Количество точек"),
                         (self.result['count_special_symbols'], len(re.findall(r"[%*&^:;№\"\'!()?@#$~{}|/-]+;", text)), "Количество спец. символов"),
                         (self.result['count_numbers'], len(re.findall(r"[0-9]", text)), "Количество цифр"),
                         (self.result['count_spaces'], text.count(" "), "Количество пробелов"),
                         (self.result['count_paragraphs'], text.count("\n") + 1, "Количество абзацев")])

    @pytest.mark.UI
    @pytest.mark.SMOKE
    @pytest.mark.parametrize(
        "text",
        [
            "Text",
            "Some text",
            "Text?",
            "интересный текст",
            "Text\n"
        ],
        ids=[
            "Normal text",
            "Text with space",
            "Text with special symbol",
            "Non ASCII symbols with space",
            "Text with paragraph"
        ]
    )
    def test_count_symbols_positive(self, text: str) -> None:
        self.prepare(text=text)
        self.do_asserts([(self.result['count_symbols'], len(''.join(text.replace('\n', ''))), "Количество символов в тексте")])

    @pytest.mark.UI
    @pytest.mark.SMOKE
    @pytest.mark.parametrize(
        "text",
        [
            "Text",
            "интересный текст",
            "Text\n"
        ],
        ids=[
            "Normal text",
            "Non ASCII symbols with space",
            "Text with paragraph"
        ]
    )
    def test_count_symbols_without_spaces_positive(self, text: str) -> None:
        self.prepare(text=text)
        self.do_asserts([(self.result['count_symbols_without_spaces'], len(''.join([text.replace(' ', '').replace('\n', '')])), "Количество символов в тексте без пробела")])

    @pytest.mark.UI
    @pytest.mark.SMOKE
    @pytest.mark.parametrize(
        "text",
        [
            "Text",
            "интересный текст",
            "Text\nText 2"
        ],
        ids=[
            "Normal text",
            "Non ASCII symbols with space",
            "Text with paragraph"
        ]
    )
    def test_count_words_positive(self, text: str) -> None:
        self.prepare(text=text)
        self.do_asserts([(self.result['count_words'], len(text.replace('\n', ' ').split(' ')), "Проверка количества слов в тексте")])

    @pytest.mark.UI
    @pytest.mark.SMOKE
    @pytest.mark.parametrize(
        "text",
        [
            "Text",
            "Text, text and text"
        ],
        ids=[
            "Normal text without commas",
            "Text with two commas"
        ]
    )
    def test_count_of_commas_positive(self, text: str) -> None:
        self.prepare(text=text)
        self.do_asserts([(self.result['count_of_commas'], text.count(','), "Проверка количества запятых")])

    @pytest.mark.UI
    @pytest.mark.SMOKE
    @pytest.mark.parametrize(
        "text",
        [
            "Text",
            "Text."
        ],
        ids=[
            "Normal text without commas",
            "Text with two commas"
        ]
    )
    def test_count_of_dots_positive(self, text: str) -> None:
        self.prepare(text=text)
        self.do_asserts([(self.result['count_of_dots'], text.count('.'), "Количество точек в тексте")])

    @pytest.mark.UI
    @pytest.mark.SMOKE
    @pytest.mark.parametrize(
        "text",
        [
            "Text",
            "Text."
        ],
        ids=[
            "Normal text",
            "Text with special symbols"
        ]
    )
    def test_special_symbols(self, text: str) -> None:
        self.prepare(text=text)
        self.do_asserts([(self.result['count_special_symbols'], len(re.findall(r"[%*&^:;№\"\'!()?@#$~{}|/-]+;", text)), "Количество спец. символов")])

    @pytest.mark.UI
    @pytest.mark.SMOKE
    @pytest.mark.parametrize(
        "text",
        [
            "Text",
            "Text 123"
        ],
        ids=[
            "Normal text",
            "Text with numbers"
        ]
    )
    def test_count_numbers_positive(self, text: str) -> None:
        self.prepare(text=text)
        self.do_asserts([(self.result['count_numbers'], len(re.findall(r"[0-9]", text)), "Проверка количества символов")])

    @pytest.mark.UI
    @pytest.mark.SMOKE
    @pytest.mark.parametrize(
        "text",
        [
            "Text",
            "Text 123",
            "Text\nText"
        ],
        ids=[
            "Normal text",
            "Text with space",
            "Text with paragraph"
        ]
    )
    def test_count_spaces_positive(self, text: str) -> None:
        self.prepare(text)
        self.do_asserts([(self.result['count_spaces'], text.count(" "), "Проверка количества пробелов")])

    @pytest.mark.UI
    @pytest.mark.SMOKE
    @pytest.mark.parametrize(
        "text",
        [
            "Text",
            "Text\n"
        ],
        ids=[
            "Normal text by one paragraph",
            "Text with one paragraph"
        ]
    )
    def test_count_paragraphs_positive(self, text: str) -> None:
        self.prepare(text)
        self.do_asserts([(self.result['count_paragraphs'], text.count('\n') + 1, "Количество параграфов в тексте")])


class TestCaseNegative(BaseTest):

    @pytest.mark.UI
    @pytest.mark.SMOKE
    @pytest.mark.parametrize("text", [""], ids=["Text is nullptr"])
    def test_null_str_negative(self, text: str) -> None:
        # Выполняем негативный тест и получаем результат.
        self.main_page.exec_query(text=text)

        # Находим поле с ошибкой.
        self.main_page.find_element(locator=self.main_page.locators.LABEL_ERROR)
