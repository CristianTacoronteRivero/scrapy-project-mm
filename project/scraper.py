import sys, os
from typing import List, Tuple
import pandas as pd
import logging

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.webdriver.chrome.service import Service

# from selenium.webdriver.common.by import By

# Agregar la ruta de la carpeta al principio de sys.path
ruta_carpeta = os.getcwd()
# La posicion 0 se encuentra reservada
sys.path.append(ruta_carpeta)

# Agregar la ruta de la carpeta al final de os.environ["PYTHONPATH"]
# OJO: se debe de hacer de esta forma ya que se trata de un entorno virtual
if "PYTHONPATH" in os.environ and not ruta_carpeta in os.environ["PYTHONPATH"]:
    os.environ["PYTHONPATH"] += os.pathsep + ruta_carpeta
else:
    os.environ["PYTHONPATH"] = ruta_carpeta

from func import custom_func


class EmptyResult(Exception):
    pass


class Scraper:
    def __init__(self, path_service=str, headless: bool = True):
        # service = Service(path_service)

        # Configurar capacidades para el controlador de Chrome
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities["goog:loggingPrefs"] = {"browser": "ALL"}

        options = Options()
        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(
            options=options, desired_capabilities=capabilities
        )

    def scrape(self, url) -> List[Tuple[str, str]]:
        self.driver.get(url)

        # Obtener el contenido HTML renderizado
        html_content = self.driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")

        # Encuentra todos los elementos que contienen la información de los smartphones
        products = soup.select(".snize-product")

        # Extrae el nombre del modelo y el precio de cada producto
        products_scraper = list()
        for product in products:
            try:
                model_name = product.select_one(".snize-title").get_text(
                    strip=True
                )
                big_price_raw = product.select_one(".snize-price").get_text(
                    strip=True
                )
                big_price = (
                    big_price_raw.replace("€", "")
                    .replace(",", "")
                    .replace(".", ",")
                )

                products_scraper.append((model_name, big_price))
            except Exception as e:
                print(f"Error al procesar el producto: {e}")

        return products_scraper

    def __del__(self):
        self.driver.quit()


if __name__ == "__main__":
    print("¡Inicio de proceso!")
    custom_func.create_logging(os.path.basename(__file__))

    data = list()

    scraper = Scraper(path_service="")

    PAG = 1
    while True:
        try:
            result = scraper.scrape(
                f"https://canarias.mediamarkt.es/collections/smartphones?tab=products&page={PAG}"
            )
            # Comprueba si ha llegado al final
            if not result:
                raise EmptyResult()
            # Concatena los datos
            data += result
            logging.info(f"Página {PAG} escrapeada correctamente")
            # Incrementa en +1 la pagina
            PAG += 1
        # Captura cualquier error inesperado
        except EmptyResult:
            logging.warning(f"Fin de scrapeo en la página {PAG - 1}")
            break
        except Exception as e:
            logging.error(f"Error inesperado. Total: {PAG - 1}")
            break

    data_frame = pd.DataFrame(data, columns=["device", "price"])
    print(data_frame)
