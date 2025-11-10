# src/bot.py
import json
import os
import random
import logging
from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from .scrapers import scrape_mercadolivre, scrape_amazon, _random_sleep
from .utils import append_history, now_iso

from .email_alert import send_price_alert

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

def load_config():
    cfg_path = os.path.join(PROJECT_ROOT, "config.json")
    with open(cfg_path, "r", encoding="utf-8") as f:
        return json.load(f)

def make_driver(headless=True):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    # minimal user-agent rotation
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    ]
    opts.add_argument(f"user-agent={random.choice(user_agents)}")
    # optional headless detection reduction
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    # try to reduce detection
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """
    })
    return driver

def run_once():
    cfg = load_config()
    headless = cfg.get("run_options", {}).get("headless", True) if "run_options" in cfg else True
    sources = cfg.get("sources", ["mercadolivre", "amazon"])
    price_limits = cfg.get("price_limit", {})
    email_cfg = cfg.get("email", {})
    products = cfg.get("products", [])

    driver = make_driver(headless=headless)
    rows = []
    try:
        for product in products:
            logging.info("Checking product: %s", product)
            _random_sleep(1.0, 2.5)

            item_results = []
            # Mercado Livre
            if "mercadolivre" in sources:
                res = scrape_mercadolivre(driver, product)
                if res and res.get("price") is not None:
                    item_results.append(res)
                    print(f"[{now_iso()}] {product} → R$ {res['price']} (MercadoLivre)")

            # Amazon
            if "amazon" in sources:
                res = scrape_amazon(driver, product)
                if res and res.get("price") is not None:
                    item_results.append(res)
                    print(f"[{now_iso()}] {product} → R$ {res['price']} (Amazon)")

            if not item_results:
                print(f"[{now_iso()}] {product} → R$ None (nenhum resultado)")
                continue

            # pega o menor preço dentre os achados
            best = min(item_results, key=lambda x: x["price"] if x["price"] is not None else float("inf"))

            row = {
                "timestamp": now_iso(),
                "product": product,
                "price": best["price"],
                "source": best["source"],
                "url": best.get("url", "")
            }
            rows.append(row)

            # print resumido (melhor encontrado)
            print(f"[{row['timestamp']}] BEST {product} → R$ {row['price']} ({row['source']})")

            # alerta por e-mail
            limit = price_limits.get(product)
            if limit is not None and row["price"] is not None and email_cfg.get("enabled", False):
                if row["price"] <= limit:
                    subject = f"ALERTA: {product} atingiu R$ {row['price']}"
                    body = f"Produto: {product}\nPreço: R$ {row['price']}\nFonte: {row['source']}\nURL: {row.get('url')}\n\nExtraído em {row['timestamp']}"
                    try:
                        send_price_alert(email_cfg.get("receiver"), subject, body)
                        print(f"📧 Alerta enviado para {email_cfg.get('receiver')}")
                    except Exception:
                        logging.exception("Falha ao enviar alerta")

    finally:
        driver.quit()

    if rows:
        append_history(rows)
        print(f"\n✅ Histórico atualizado ({len(rows)} linhas) em LOGS/history.csv")
    else:
        print("\n⚠️ Nenhum resultado salvo.")

if __name__ == "__main__":
    run_once()
