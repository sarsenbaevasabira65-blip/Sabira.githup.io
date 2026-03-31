import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes,
)

# ========================
# ⚙️ БАПТАУЛАР
# ========================
BOT_TOKEN = "YOUR_BOT_TOKEN"
ADMIN_ID = 123456789

BUSINESS_NAME = "Сенің идеяң — біздің өнер 🎨"

KASPI_NUMBER = "+77000000000"
KASPI_NAME = "Your Name"

# ========================
# 📋 SERVICES
# ========================
SERVICES = {
    "photo": {
        "name_kz": "🖼 Фото жасау (AI)",
        "name_ru": "🖼 Генерация фото (AI)",
        "price_kz": "1 фото — 2 000 ₸",
        "price_ru": "1 фото — 2 000 ₸",
    },
    "video": {
        "name_kz": "🎬 Видео жасау (AI)",
        "name_ru": "🎬 Создание видео (AI)",
        "price_kz": "15 сек — 5 000 ₸",
        "price_ru": "15 сек — 5 000 ₸",
    },
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
        [InlineKeyboardButton("💳 Төлеу / Оплатить", callback_data=f"pay_{svc}_{lang}")],
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

    # Тіл таңдау
    if data.startswith("lang_"):
        lang = data.split("_")[1]
        text = "Қызмет таңдаңыз" if lang == "kz" else "Выберите услугу"

        await query.edit_message_text(
            text,
            reply_markup=main_menu_keyboard(lang)
        )

    # Қызмет
    elif data.startswith("svc_"):
        _, svc, lang = data.split("_")

        text = (
            SERVICES[svc]["name_kz"] + "\n\n" + SERVICES[svc]["price_kz"]
            if lang == "kz"
            else SERVICES[svc]["name_ru"] + "\n\n" + SERVICES[svc]["price_ru"]
        )

        await query.edit_message_text(
            text,
            reply_markup=service_keyboard(lang, svc)
        )

    # Төлем
    elif data.startswith("pay_"):
        _, svc, lang = data.split("_")

        text = (
            f"📱 Kaspi:\n{KASPI_NUMBER}\n{KASPI_NAME}\n\nСкрин жіберіңіз"
            if lang == "kz"
            else f"📱 Kaspi:\n{KASPI_NUMBER}\n{KASPI_NAME}\n\nОтправьте скрин"
        )

        await query.edit_message_text(text)

    # Менеджер
    elif data.startswith("manager_"):
        lang = data.split("_")[1]

        text = (
            f"📞 Менеджер: {KASPI_NUMBER}"
            if lang == "kz"
            else f"📞 Менеджер: {KASPI_NUMBER}"
        )

        await query.edit_message_text(text, reply_markup=back_keyboard(lang))

    # Артқа
    elif data.startswith("back_"):
        lang = data.split("_")[1]

        await query.edit_message_text(
            "Қызмет таңдаңыз" if lang == "kz" else "Выберите услугу",
            reply_markup=main_menu_keyboard(lang)
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = update.message

    await context.bot.send_message(
        ADMIN_ID,
        f"👤 {user.full_name}\n@{user.username}"
    )

    await context.bot.forward_message(
        ADMIN_ID,
        msg.chat_id,
        msg.message_id
    )

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
    main()
