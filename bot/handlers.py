import tempfile
import pandas as pd
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.helpers import escape_markdown
from .db     import save_sources
from .parser import compute_average_prices

async def start(update: Update):
    kb = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton("Загрузить файл", callback_data='upload')
    )
    await update.message.reply_text(
        "Нажми кнопку ниже, чтобы загрузить Excel‑файл с источниками.",
        reply_markup=kb
    )


async def button_handler(update: Update):
    query = update.callback_query
    await query.answer()
    if query.data == 'upload':
        await query.edit_message_text("Пришлите Excel‑файл (.xlsx) с полями title, url, xpath.")


async def file_handler(update: Update):
    document = update.message.document
    if not document.file_name.lower().endswith(('.xlsx', '.xls')):
        await update.message.reply_text("Ожидаю Excel‑файл.")
        return

    f = await document.get_file()
    tmp = tempfile.NamedTemporaryFile(suffix=document.file_name, delete=False)
    await f.download_to_drive(tmp.name)
    tmp.close()

    try:
        df = pd.read_excel(tmp.name, engine='openpyxl')
    except Exception as e:
        await update.message.reply_text(f"Ошибка чтения Excel: {e}")
        return

    required = {'title', 'url', 'xpath'}
    if not required.issubset(df.columns):
        missing = required - set(df.columns)
        await update.message.reply_text(f"В файле не хватает колонок: {missing}")
        return

    raw_md = df.to_markdown(index=False)
    safe_md = escape_markdown(raw_md, version=2)
    await update.message.reply_text(
        f"Содержимое файла:*\n```{safe_md}```",
        parse_mode="MarkdownV2"
    )

    save_sources(df)

    avg_df = compute_average_prices(df)
    raw_md2 = avg_df.to_markdown(index=False)
    safe_md2 = escape_markdown(raw_md2, version=2)
    await update.message.reply_text(
        f"Средняя цена по каждому сайту:*\n```{safe_md2}```",
        parse_mode="MarkdownV2"
    )
