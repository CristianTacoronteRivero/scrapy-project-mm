from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class Scraper:
    def __init__(self, headless=True):
        options = Options()
        if headless:
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            "/usr/lib/chromium-browser/chromedriver", options=options
        )

    def scrape(self, url):
        self.driver.get(url)
        # Aquí puedes usar los métodos de Selenium, por ejemplo:
        element = self.driver.find_element(
            By.CSS_SELECTOR, ".snize-overhidden"
        )
        return element.text

    def __del__(self):
        self.driver.quit()


if __name__ == "__main__":
    # Aquí puedes crear una instancia de la clase Scraper y llamar al método scrape.
    scraper = Scraper()
    result = scraper.scrape(
        "https://canarias.mediamarkt.es/collections/smartphones?tab=products&page=1"
    )
    print(result)
