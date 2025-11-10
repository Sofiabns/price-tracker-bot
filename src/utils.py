# src/utils.py
import re
import logging
from datetime import datetime
import os
import pandas as pd

LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "LOGS")
HISTORY_PATH = os.path.join(LOGS_DIR, "history.csv")

def ensure_logs_dir():
    os.makedirs(LOGS_DIR, exist_ok=True)

def now_iso():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def sanitize_price(text: str):
    """
    Converte strings como 'R$ 1.234,56', 'R$1.234', '1.234,56', 'R$ 1.234' para float.
    Retorna None se falhar.
    """
    if text is None:
        return None
    try:
        s = str(text)
        # remove non-numeric except , and .
        s = s.replace("R$", "").replace("\xa0", "").strip()
        # heurística: se tem ',' e ',' está depois do último '.', então provavelmente BR format
        # remove espaços e símbolos
        s = re.sub(r"[^\d,\.]", "", s)
        # if comma exists and is decimal separator (ex: '1.234,56')
        if "," in s and s.rfind(",") > s.rfind("."):
            s = s.replace(".", "")
            s = s.replace(",", ".")
        else:
            s = s.replace(",", "")
        return float(s)
    except Exception:
        logging.exception("sanitize_price failed for: %s", text)
        return None

def append_history(rows: list[dict]):
    """
    rows: list of dicts with keys: timestamp, product, price, source, url
    """
    ensure_logs_dir()
    df_new = pd.DataFrame(rows)
    if os.path.exists(HISTORY_PATH):
        df_existing = pd.read_csv(HISTORY_PATH)
        df = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df = df_new
    df.to_csv(HISTORY_PATH, index=False)
