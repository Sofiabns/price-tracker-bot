# src/scheduler.py
import schedule
import time
from .bot import run_once

def job():
    print("Starting scheduled run...")
    try:
        run_once()
    except Exception as e:
        print("Scheduled run failed:", e)

# Exemplo: rodar todo dia às 08:00
schedule.every().day.at("08:00").do(job)

if __name__ == "__main__":
    print("Scheduler started. Ctrl+C para sair.")
    while True:
        schedule.run_pending()
        time.sleep(1)
