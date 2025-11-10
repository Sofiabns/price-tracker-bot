# src/scrapers.py
import time
import random
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .utils import sanitize_price

def _random_sleep(a=0.6, b=1.6):
    time.sleep(random.uniform(a, b))

def scrape_mercadolivre(driver, query, wait_seconds=8):
    """
    Retorna dict { price: float, url: str, source: 'mercadolivre' } ou None.
    Usa lista (search) do Mercado Livre.
    """
    try:
        q = query.replace(" ", "-")
        url = f"https://lista.mercadolivre.com.br/{q}"
        driver.get(url)
        WebDriverWait(driver, wait_seconds).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ol.ui-search-layout"))
        )
        _random_sleep()
        # tenta localizar primeiro resultado com preço
        items = driver.find_elements(By.CSS_SELECTOR, "ol.ui-search-layout li.ui-search-layout__item")
        if not items:
            items = driver.find_elements(By.CSS_SELECTOR, "ol.ui-search-layout li")
        for item in items:
            try:
                # preço: fraction + cents
                frac = item.find_element(By.CSS_SELECTOR, "span.price-tag-fraction").text
                # alguns anúncios não têm cents
                try:
                    cents = item.find_element(By.CSS_SELECTOR, "span.price-tag-cents").text
                    price_text = f"{frac},{cents}"
                except Exception:
                    price_text = frac
                link = item.find_element(By.CSS_SELECTOR, "a.ui-search-link").get_attribute("href")
                price = sanitize_price(price_text)
                if price is not None:
                    return {"price": price, "url": link, "source": "mercadolivre"}
            except Exception:
                continue
        return None
    except Exception:
        logging.exception("mercadolivre scraper failed for %s", query)
        return None

def scrape_amazon(driver, query, wait_seconds=8):
    """
    Retorna dict { price: float, url: str, source: 'amazon' } ou None.
    Usa Amazon Brasil (s=k=).
    """
    try:
        q = query.replace(" ", "+")
        url = f"https://www.amazon.com.br/s?k={q}"
        driver.get(url)
        WebDriverWait(driver, wait_seconds).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot"))
        )
        _random_sleep()
        containers = driver.find_elements(By.CSS_SELECTOR, "div.s-main-slot div.s-result-item")
        if not containers:
            return None
        for item in containers:
            try:
                # prioridade: a-offscreen (preço completo)
                try:
                    price_text = item.find_element(By.CSS_SELECTOR, "span.a-offscreen").get_attribute("innerText")
                except Exception:
                    # fallback para whole + fraction
                    whole = item.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
                    frac = item.find_element(By.CSS_SELECTOR, "span.a-price-fraction").text
                    price_text = f"{whole}.{frac}"
                link = ""
                try:
                    link_tag = item.find_element(By.CSS_SELECTOR, "h2 a")
                    link = link_tag.get_attribute("href")
                except Exception:
                    pass
                price = sanitize_price(price_text)
                if price is not None:
                    return {"price": price, "url": link, "source": "amazon"}
            except Exception:
                continue
        return None
    except Exception:
        logging.exception("amazon scraper failed for %s", query)
        return None
