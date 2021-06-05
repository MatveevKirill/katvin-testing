from selenium.webdriver.common.by import By


class MainPageLocators(object):
    INPUT_TEXT = (By.ID, 'textsymbols')
    BUTTON_RUN = (By.ID, 'run')
    BLOCK_RESULT = (By.ID, 'result')

    LABEL_ROW_TEMPLATE = (By.XPATH, '//tbody[@class = "brd"]/tr[{}]/td[2]')
    LABEL_ERROR = (By.XPATH, "//div[@id = 'result']/div[@class = 'alert alert-danger']")
