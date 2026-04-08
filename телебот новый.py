Python 3.13.3 (tags/v3.13.3:6280bb5, Apr  8 2025, 14:47:33) [MSC v.1943 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes,
)

# ========================
# ⚙️ БАПТАУЛАР
# ========================
BOT_TOKEN = "8754227384:AAEUXtTBoOVajScixmGg-ccRV086mUQ5zrw"
ADMIN_ID = 1313252587
OPENAI_API_KEY = "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"

BUSINESS_NAME = "AI Creative Bot"

KASPI_NUMBER = "+77474513371"
KASPI_NAME = "Сабира С"

# ========================
# 📊 DATA (mini CRM)
# ========================
orders = {}
users = {}

# ========================
# 📋 SERVICES
# ========================
SERVICES = {
    "photo": "🖼 AI Фото (200-2000 ₸)",
    "video": "🎬 AI Видео (2000-5000 ₸)",
    "bot": "🤖 Telegram бот (20 000 ₸ бастап)",
    "site": "🌐 Сайт (30 000 ₸ бастап)"
}

# ========================
# ⌨️ MENU
# ========================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🖼 Фото", callback_data="svc_photo")],
        [InlineKeyboardButton("🎬 Видео", callback_data="svc_video")],
        [InlineKeyboardButton("🤖 Бот", callback_data="svc_bot")],
        [InlineKeyboardButton("🌐 Сайт", callback_data="svc_site")],
        [InlineKeyboardButton("📞 Менеджер", callback_data="manager")]
    ])

# ========================
# 📨 START
# ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👋 {BUSINESS_NAME}\n\nҚош келдіңіз!\nҚызмет таңдаңыз 👇",
        reply_markup=main_menu()
    )

# ========================
# 🔘 BUTTONS
# ========================
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    user_id = query.from_user.id

    if data.startswith("svc_"):
        svc = data.split("_")[1]

        orders[user_id] = {
            "service": svc,
            "status": "started"
        }

        await query.edit_message_text(
            f"✅ {SERVICES[svc]} таңдадыңыз\n\n📩 Толығырақ жазыңыз (мысалы: стиль, тема)"
        )

    elif data == "manager":
        await query.edit_message_text(
            f"📞 Менеджер: {KASPI_NUMBER}",
            reply_markup=main_menu()
        )

# ========================
# 🤖 AI + ЗАКАЗ
# ========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    user_id = msg.from_user.id

    # заказ логика
    if user_id in orders:
...         if orders[user_id]["status"] == "started":
...             orders[user_id]["details"] = msg.text
...             orders[user_id]["status"] = "waiting_payment"
... 
...             await msg.reply_text(
...                 f"💳 Төлем жасаңыз:\n{KASPI_NUMBER}\n{KASPI_NAME}\n\nСосын чек жіберіңіз 📸"
...             )
...             return
... 
...     # админге жіберу
...     await context.bot.forward_message(ADMIN_ID, msg.chat_id, msg.message_id)
... 
...     # AI жауап
...     try:
...         from openai import OpenAI
...         client = OpenAI(api_key=OPENAI_API_KEY)
... 
...         system_prompt = f"""
... Сен — {BUSINESS_NAME} кәсіби сатушысың.
... 
... Мақсат:
... - Клиентті заказға жеткізу
... 
... Стиль:
... - Сыпайы
... - Қысқа
... - Сенімді
... 
... Қызметтер:
... - AI фото
... - AI видео
... - Бот жасау
... - Сайт жасау
... 
... Ереже:
... - Әр жауап соңында сұрақ қой
... - Клиентті қызықтыр
... 
... Возражение:
"қымбат" → "жеңіл нұсқа ұсынайын ба?"
"ойланам" → "қазір бастайық па?"
"керек емес" → "пайдасын көрсет"

"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": msg.text}
            ]
        )

        await msg.reply_text(response.choices[0].message.content)

    except Exception as e:
        print(e)
        await msg.reply_text("✅ Қабылданды")

# ========================
# 💳 ЧЕК ҚАБЫЛДАУ
# ========================
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    user_id = msg.from_user.id

    if user_id in orders and orders[user_id]["status"] == "waiting_payment":

        orders[user_id]["status"] = "paid"

        await context.bot.send_message(
            ADMIN_ID,
            f"💰 Жаңа төлем!\nUser: {user_id}\nService: {orders[user_id]['service']}\nDetails: {orders[user_id].get('details','')}"
        )

        await context.bot.forward_message(
            ADMIN_ID,
            msg.chat_id,
            msg.message_id
        )

        await msg.reply_text("✅ Төлем қабылданды! Жұмыс басталды 🚀")

    else:
        await msg.reply_text("❗ Алдымен заказ жасаңыз")

# ========================
# 🎯 FOLLOW-UP
# ========================
async def follow_up(context: ContextTypes.DEFAULT_TYPE):
    for user_id, data in orders.items():
        if data["status"] == "started":
            try:
                await context.bot.send_message(
                    user_id,
                    "😊 Заказты аяқтамадыңыз. Жалғастырамыз ба?"
                )
            except:
                pass

# ========================
# 🚀 MAIN
# ========================
def main():
    logging.basicConfig(level=logging.INFO)

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # авто напоминание
    app.job_queue.run_repeating(follow_up, interval=3600, first=60)

    print("🔥 Бот іске қосылды")
    app.run_polling()

if __name__ == "__main__":
