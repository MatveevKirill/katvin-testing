from ui.locators.PageLocators import MainPageLocators
from ui.pages.base_page import BasePageActions


class MainPage(BasePageActions):
    url = 'https://katvin.com/tools/number-characters.html'
    locators = MainPageLocators

    def exec_query(self, text: str, auto_clear: bool = True) -> None:
        """
        Отправление данные в текстовое поле.
        :param auto_clear: автоматическая очистка поля для ввода.
        :param text: текст для отправки.
        :return: None
        """
        self.send_keys(self.locators.INPUT_TEXT, text, auto_clear=auto_clear)
        self.click(self.locators.BUTTON_RUN)

    def get_results(self):
        """
        Получение результата из тестовых полей.
        :return: dict -> |количество символов, количество символов без пробела, количество слов, количество запятых,
                          количество точек, количество спецсимволов, количество цифр, количество пробелов,
                          количество абзацев|
        """

        return {
            'count_symbols': int(self.get_text_from_element(locator=(self.locators.LABEL_ROW_TEMPLATE[0],
                                                                 self.locators.LABEL_ROW_TEMPLATE[1].format(1)))),
            'count_symbols_without_spaces': int(self.get_text_from_element(locator=(self.locators.LABEL_ROW_TEMPLATE[0],
                                                                                self.locators.LABEL_ROW_TEMPLATE[1].format(2)))),
            'count_words': int(self.get_text_from_element(locator=(self.locators.LABEL_ROW_TEMPLATE[0],
                                                               self.locators.LABEL_ROW_TEMPLATE[1].format(3)))),
            'count_of_commas': int(self.get_text_from_element(locator=(self.locators.LABEL_ROW_TEMPLATE[0],
                                                                   self.locators.LABEL_ROW_TEMPLATE[1].format(4)))),
            'count_of_dots': int(self.get_text_from_element(locator=(self.locators.LABEL_ROW_TEMPLATE[0],
                                                                 self.locators.LABEL_ROW_TEMPLATE[1].format(5)))),
            'count_special_symbols': int(self.get_text_from_element(locator=(self.locators.LABEL_ROW_TEMPLATE[0],
                                                                         self.locators.LABEL_ROW_TEMPLATE[1].format(6)))),
            'count_numbers': int(self.get_text_from_element(locator=(self.locators.LABEL_ROW_TEMPLATE[0],
                                                                 self.locators.LABEL_ROW_TEMPLATE[1].format(7)))),
            'count_spaces': int(self.get_text_from_element(locator=(self.locators.LABEL_ROW_TEMPLATE[0],
                                                                self.locators.LABEL_ROW_TEMPLATE[1].format(8)))),
            'count_paragraphs': int(self.get_text_from_element(locator=(self.locators.LABEL_ROW_TEMPLATE[0],
                                                                    self.locators.LABEL_ROW_TEMPLATE[1].format(9))))
        }
