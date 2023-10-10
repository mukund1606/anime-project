from selenium import webdriver

# Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions


class Browser:
    def __init__(self) -> None:
        self.chrome_options = ChromeOptions()
        self.chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-logging"]
        )
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_experimental_option("detach", True)
        self.chrome_service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(
            service=self.chrome_service, options=self.chrome_options
        )
