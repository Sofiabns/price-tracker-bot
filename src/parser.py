from selenium.webdriver.common.by import By
from utils import sanitize_price
import time

def extract_google_price(driver, product):
    driver.get(f"https://www.google.com/search?q={product}+preço")
    time.sleep(2.5)

    # 🔍 Captura tudo que pareça preço
    elements = driver.find_elements(By.XPATH, "//*[contains(text(),'R$')]")

    # Debug: imprime tudo
    print("\n### DEBUG: elementos encontrados ###")
    for e in elements:
        print("→", e.text)

    # Tenta extrair o primeiro possível
    for e in elements:
        p = sanitize_price(e.text)
        if p:
            return p

    return None
