# zyuzublik-bot

Telegram‑бот для приёма Excel‑файла с сайтами, парсинга цен и расчёта средней цены.

## Структура

- `bot/`  
  ├── `config.py` — константы и токен  
  ├── `db.py`     — инициализация и сохранение в SQLite  
  ├── `parser.py` — функции парсинга и вычисления средних  
  ├── `handlers.py` — Telegram‑хендлеры  
  └── `main.py`   — точка входа  

## Установка

```bash
git clone https://github.com/yourusername/zyuzublik-bot.git
cd zyuzublik-bot

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export BOT_TOKEN="ваш_токен"
# (опционально) export DB_PATH="путь/до/data.db"

python -m bot.main
