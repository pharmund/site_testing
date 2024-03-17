from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import re
import os


class TextAnalyzer:
    def __init__(self):
        self.driver = None

    def start_driver(self):
        options = webdriver.ChromeOptions()
        options.binary_location = "C:\\Users\\Redmi\\Desktop\\yandexdriver.exe"
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def stop_driver(self):
        if self.driver:
            self.driver.quit()

    def analyze_text(self, text):
        self.driver.get("http://www.pharmund.ru/")
        time.sleep(2)
        field = self.driver.find_element(By.XPATH, "/html/body/form[1]/table/tbody/tr/td[2]/input")

        # Использование JavaScript для вставки текста
        self.driver.execute_script('arguments[0].value=arguments[1]', field, text)
        time.sleep(1)

        # Нажимаем на кнопку
        button = self.driver.find_element(By.XPATH, '/html/body/form[1]/p[3]/input')
        button.click()

        time.sleep(3)

        # находим элемент, содержащий текст
        result_element = self.driver.find_element(By.XPATH, '/html/body/p[1]')

        # записываем в переменную result_phrase текст из элемента result_element
        result_phrase = result_element.text

        # с помощью assert проверяет, что ожидаемый текст совпадает с текстом на странице сайта
        assert "The following results are returned:" == result_phrase

        # Проверяет, что количество слов больше или равно 0
        elements = [
            ('/html/body/center[3]/table/tbody/tr/td[2]', 0),
            ('/html/body/center[3]/table/tbody/tr/td[4]', 0),
            ('/html/body/center[3]/table/tbody/tr/td[6]', 0),
            ('/html/body/center[3]/table/tbody/tr/td[8]', 0),
            ('/html/body/center[3]/table/tbody/tr/td[10]', 0),
            ('/html/body/center[3]/table/tbody/tr/td[12]', 0),
            ('/html/body/center[3]/table/tbody/tr/td[14]', 0),
            ('/html/body/center[3]/table/tbody/tr/td[16]', 0)
        ]
        for xpath, expected_value in elements:
            element = self.driver.find_element(By.XPATH, xpath)
            assert int(element.text) >= expected_value

    def take_screenshot(self, text_file_path):
        """Делает скриншот"""
        screenshot_path = 'screenshots/' + re.search(r'[^/\\]+(?=\.\w+$)', text_file_path).group(0) + '.png'
        self.driver.save_screenshot(screenshot_path)

    def go_back(self):
        """"Возвращается на предыдущую страницу"""
        self.driver.back()

    def clear_field(self):
        """"Очищает поле"""
        element = self.driver.find_element(By.XPATH, "/html/body/form[1]/table/tbody/tr/td[2]/input")
        element.clear()
        time.sleep(1)

    def run(self, text_file_path):
        with open(text_file_path, "r") as file:
            text = file.read()
            self.analyze_text(text)
            self.take_screenshot(text_file_path)
            self.driver.back()
            self.clear_field()


if __name__ == "__main__":
    books_directory_path = "texts/"
    books = os.listdir(books_directory_path)
    analyzer = TextAnalyzer()
    analyzer.start_driver()
    for book in books:
        analyzer.run(f"texts/{book}")
    analyzer.stop_driver()