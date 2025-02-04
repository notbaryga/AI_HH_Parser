from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support import expected_conditions as EC

from ai_api import get_letter

class Parser:
    def __init__(self):
        self.driver = self.create_driver_instance()

    @classmethod
    def create_driver_instance(cls):
        drive_options = cls.get_options()
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=drive_options)
        return driver

    @classmethod
    def get_options(cls):
        drive_options = Options()
        drive_options.add_argument("--no-sandbox")
        # drive_options.add_argument("--headless=new")
        drive_options.add_argument("--disable-cache")
        drive_options.add_argument("--disable-dev-shm-usage")
        drive_options.add_argument("--ignore-certificate-errors")

        return drive_options

    def wait_for_page_load(self, timeout: int = 15) -> None:
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "html"))
        )

    def get_all_links(self):
        self.driver.get('https://hh.ru/search/vacancy')
        self.wait_for_page_load()
        links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href^="https://ekaterinburg.hh.ru/vacancy/"]')
        return links

    def process_vacancy(self, url):
        self.driver.get(url)
        vacancy_text = None

        letter = get_letter(vacancy_text)

        button = self.driver.find_element(By.CSS_SELECTOR, 'a[data-qa="vacancy-response-link-top"]')
        button.click()

        letter_button = self.driver.find_element(By.CSS_SELECTOR, 'button.bloko-button.bloko-button_kind-primary')
        letter_button.click()



