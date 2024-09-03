# utils/selenium_utils.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import CHROME_DRIVER_PATH
from datetime import datetime

# Configuración de Selenium
chrome_options = Options()
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")
service = Service(CHROME_DRIVER_PATH)


def wait_for_element(browser, locator, timeout=10):
    return WebDriverWait(browser, timeout).until(
        EC.presence_of_element_located(locator)
    )

# Función para buscar trenes usando Selenium
def buscar_trenes(origen, destino, fecha):
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.get("https://www.renfe.com/es/es")
    
    origen_input = wait_for_element(browser, (By.ID, "origin"))
    destino_input = wait_for_element(browser, (By.ID, "destination"))
    fecha_ida_input = wait_for_element(browser, (By.ID, "first-input"))
    submit_button = wait_for_element(browser, (By.CLASS_NAME, "mdc-button__touch.sc-rf-button"))

    origen_input.clear()
    origen_input.send_keys(origen)
    origen_input.send_keys(Keys.ARROW_DOWN)
    origen_input.send_keys(Keys.ENTER)

    destino_input.clear()
    destino_input.send_keys(destino)
    destino_input.send_keys(Keys.ARROW_DOWN)
    destino_input.send_keys(Keys.ENTER)

    accept_cookies_button = browser.find_element(By.ID, "onetrust-reject-all-handler")
    accept_cookies_button.click()

    browser.implicitly_wait(2)
    fecha_ida_input.click()

    fecha_ida_input.send_keys(Keys.UP)
    fecha_ida_input = wait_for_element(browser, (By.CLASS_NAME, "rf-daterange-picker-alternative__ipt"))
    dias_diferencia = calcular_diferencia_fecha(fecha)
    for dia in range(dias_diferencia + 1):
        fecha_ida_input.send_keys(Keys.RIGHT)

    submit_button.click()

    trenes = obtener_trenes_completos(browser)
    browser.quit()
    return trenes

# Función para calcular la diferencia entre fechas
def calcular_diferencia_fecha(fecha_string):
    fecha_introducida = datetime.strptime(fecha_string, "%d/%m/%Y")
    fecha_actual = datetime.now()
    diferencia = fecha_introducida - fecha_actual 
    return diferencia.days

# Función para obtener la lista de trenes disponibles
def obtener_trenes_completos(browser):
    trenes = []
    tren_principal = browser.find_element(By.ID, "listaTrenesTBodyIda")
    trenes_divs = tren_principal.find_elements(By.CSS_SELECTOR, f"[id^='tren_i_']")
    
    for tren_div in trenes_divs:
        tren = {}
        tren["numero"] = int(tren_div.get_attribute("id").split("_")[2])
        titulo_tren = tren_div.find_element(By.CSS_SELECTOR, "[id$='_item1']")
        hora_salida = titulo_tren.find_element(By.TAG_NAME, "h5").text
        tren["hora_salida"] = hora_salida
        precio_tren = tren_div.find_element(By.CSS_SELECTOR, "[id$='_item2']")
        try:
            precio_tren.find_element(By.TAG_NAME, "title")
        except:
            pass

        if "completo" in precio_tren.text.lower():
            tren["completo"] = 'No Disponible'
        else:
            if "accessible" in precio_tren.text.lower():
                tren["completo"] = 'No Disponible'
            else:
                tren["completo"] = 'Disponible'

        trenes.append(tren)
    
    return trenes