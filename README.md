# 💰 Price Tracker Bot

Bot inteligente para automação de coleta de preços de concorrentes, gerando relatórios históricos e enviando alertas quando valores atingem limites desejados. Ideal para e-commerce, varejo, dropshipping e monitoramento competitivo.

---

## 🎯 Motivação

Empresas gastam horas monitorando preços manualmente em:

- Mercado Livre
- Amazon
- Magalu
- Shopee
- Americanas

Isso resulta em:

❌ lentidão  
❌ falta de histórico  
❌ alta chance de erro humano  

O **Price Tracker Bot** automatiza esse fluxo.

---

## 🧩 Funcionalidades

- ✔ Scraping automático usando Selenium
- ✔ Histórico salvo em CSV
- ✔ Alerta de preço via e-mail
- ✔ Lista de produtos configurável
- ✔ Delay randomizado anti-ban
- ✔ Logs de execução
- ✔ Scheduler para rodar diariamente

---

## 🏛 Arquitetura

price-tracker-bot/
│
├── README.md
├── requirements.txt
├── config.json
├── LOGS/
│ └── history.csv
└── src/
├── bot.py
├── parser.py
├── email_alert.py
└── scheduler.py


---

## 🔧 Tecnologias Utilizadas

- Python 3.10+
- Selenium WebDriver
- ChromeDriver
- Pandas
- SMTP (notificações por e-mail)
- Schedule / Cron

---

## ⚙ Configuração

Edite `config.json`:

```json
{
  "products": [
    "RTX 3060",
    "Monitor Gamer 144hz",
    "PlayStation 5"
  ],
  "sources": [
    "mercadolivre",
    "amazon"
  ],
  "price_limit": {
    "RTX 3060": 2300,
    "Monitor Gamer 144hz": 900,
    "PlayStation 5": 3000
  },
  "email": {
    "enabled": true,
    "receiver": "destinatario@gmail.com"
  },
  "run_options": {
    "headless": true,
    "max_wait_seconds": 10
  }
}

🚀 Como rodar

1) Clonar o repositório

git clone https://github.com/Sofiabns/price-tracker-bot.git
cd price-tracker-bot

2) Instalar dependências

pip install -r requirements.txt

3) Instalar ChromeDriver

Linux:
sudo apt install chromedriver
Windows:
baixar em https://chromedriver.chromium.org/

4) Executar o bot

python src/bot.py

🔐 Segurança

- senha via variável de ambiente
- config externo
- email com senha de app (Gmail recomendado)

📈 Roadmap

- Dashboard Flask
- Persistência com MySQL
- Deploy em AWS Lambda
- Alertas no Telegram
- Comparativos semanais automáticos
- Gráficos históricos

👥 Impacto real
Usado por:
- analistas de pricing
- dropshippers
- marketing
- varejo competitivo
- operações de e-commerce