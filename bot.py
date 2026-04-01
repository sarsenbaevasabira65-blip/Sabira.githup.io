Python 3.13.3 (tags/v3.13.3:6280bb5, Apr  8 2025, 14:47:33) [MSC v.1943 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> import logging
... from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
... from telegram.ext import (
...     Application, CommandHandler, CallbackQueryHandler,
...     MessageHandler, filters, ContextTypes,
... )
... 
... # ========================
... # ⚙️ БАПТАУЛАР
... # ========================
... BOT_TOKEN = "8754227384:AAEUXtTBoOVajScixmGg-ccRV086mUQ5zrw"
... ADMIN_ID = 1313252587
... OPENAI_API_KEY = "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" 
... 
... BUSINESS_NAME = "Сенің идеяң — біздің өнер 🎨"
... 
... KASPI_NUMBER = "+77474513371"
... KASPI_NAME = "Сабира С"
... 
... # ========================
... # 📋 SERVICES
... # ========================
... SERVICES = {
...     "photo": {
...         "name_kz": "🖼 Фото жасау",
...         "name_ru": "🖼 Генерация фото",
...         "price_kz": "1 фото — 2000 ₸",
...         "price_ru": "1 фото — 2000 ₸",
...     },
...     "video": {
...         "name_kz": "🎬 Видео жасау",
...         "name_ru": "🎬 Создание видео",
...         "price_kz": "15 сек — 5000 ₸",
...         "price_ru": "15 сек — 5000 ₸",
...     },
}

# ========================
# ⌨️ KEYBOARDS
# ========================
def lang_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇰🇿 Қазақша", callback_data="lang_kz"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        ]
    ])

def main_menu_keyboard(lang):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🖼 Фото", callback_data=f"svc_photo_{lang}")],
        [InlineKeyboardButton("🎬 Видео", callback_data=f"svc_video_{lang}")],
        [InlineKeyboardButton("📞 Менеджер", callback_data=f"manager_{lang}")]
    ])

def service_keyboard(lang, svc):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 Тапсырыс / Төлеу", callback_data=f"pay_{svc}_{lang}")],
        [InlineKeyboardButton("⬅️ Назад", callback_data=f"back_{lang}")]
    ])

def back_keyboard(lang):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Назад", callback_data=f"back_{lang}")]
    ])

# ========================
# 📨 HANDLERS
# ========================
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👋 *{BUSINESS_NAME}*\n\nТілді таңдаңыз:",
        parse_mode="Markdown",
        reply_markup=lang_keyboard()
    )

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ТІЛ
    if data.startswith("lang_"):
        lang = data.split("_")[1]
        text = "Қызмет таңдаңыз" if lang == "kz" else "Выберите услугу"

        await query.edit_message_text(text, reply_markup=main_menu_keyboard(lang))

    # ҚЫЗМЕТ
    elif data.startswith("svc_"):
        _, svc, lang = data.split("_")

        text = (
            SERVICES[svc]["name_kz"] + "\n\n" + SERVICES[svc]["price_kz"]
            if lang == "kz"
            else SERVICES[svc]["name_ru"] + "\n\n" + SERVICES[svc]["price_ru"]
        )

        await query.edit_message_text(text, reply_markup=service_keyboard(lang, svc))

    # ТӨЛЕМ (Kaspi only)
    elif data.startswith("pay_"):
        _, svc, lang = data.split("_")

        text = (
            f"📱 Kaspi:\n{KASPI_NUMBER}\n{KASPI_NAME}\n\nСкрин жіберіңіз"
            if lang == "kz"
            else f"📱 Kaspi:\n{KASPI_NUMBER}\n{KASPI_NAME}\n\nОтправьте скрин"
        )

        await query.edit_message_text(text)

    # МЕНЕДЖЕР
    elif data.startswith("manager_"):
        lang = data.split("_")[1]

        text = (
            f"📞 Менеджер: {KASPI_NUMBER}"
        )

        await query.edit_message_text(text, reply_markup=back_keyboard(lang))

    # BACK
    elif data.startswith("back_"):
        lang = data.split("_")[1]

        await query.edit_message_text(
            "Қызмет таңдаңыз" if lang == "kz" else "Выберите услугу",
            reply_markup=main_menu_keyboard(lang)
        )

# ========================
# 📩 USER MESSAGE + AI
# ========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = update.message

    # ADMIN-ға жіберу
    await context.bot.send_message(
        ADMIN_ID,
        f"👤 {user.full_name}\n@{user.username}"
    )

    await context.bot.forward_message(
        ADMIN_ID,
        msg.chat_id,
        msg.message_id
    )

    # 🤖 AI жауап (қосуға дайын)
    try:
        import openai

        openai.api_key = OPENAI_API_KEY

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": msg.text}]
        )

        ai_reply = response.choices[0].message.content

        await msg.reply_text(ai_reply)

    except:
        await msg.reply_text("✅ Қабылданды / Принято")

# ========================
# 🚀 START
# ========================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))

    print("Бот іске қосылды ✅")
    app.run_polling()

if __name__ == "__main__":
