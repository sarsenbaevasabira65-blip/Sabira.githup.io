import logging
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
# 📋 SERVICES
# ========================
SERVICES = {
    "photo": {
        "name_kz": "🖼 Фото жасау",
        "price_kz": "1 фото — 200-2000 ₸",
    },
    "video": {
        "name_kz": "🎬 Видео жасау",
        "price_kz": "15 сек — 2000-5000 ₸",
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
        [InlineKeyboardButton("💳 Төлеу", callback_data=f"pay_{svc}_{lang}")],
        [InlineKeyboardButton("⬅️ Назад", callback_data=f"back_{lang}")]
    ])

# ========================
# 📨 HANDLERS
# ========================
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👋 {BUSINESS_NAME}\n\nТілді таңдаңыз:",
        reply_markup=lang_keyboard()
    )

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("lang_"):
        lang = data.split("_")[1]
        await query.edit_message_text(
            "Қызмет таңдаңыз",
            reply_markup=main_menu_keyboard(lang)
        )

    elif data.startswith("svc_"):
        _, svc, lang = data.split("_")

        text = SERVICES[svc]["name_kz"] + "\n\n" + SERVICES[svc]["price_kz"]

        await query.edit_message_text(text, reply_markup=service_keyboard(lang, svc))

    elif data.startswith("pay_"):
        await query.edit_message_text(
            f"📱 Kaspi:\n{KASPI_NUMBER}\n{KASPI_NAME}\n\nСкрин жіберіңіз"
        )

    elif data.startswith("manager_"):
        lang = data.split("_")[1]

        await query.edit_message_text(
            f"📞 Менеджер: {KASPI_NUMBER}",
            reply_markup=main_menu_keyboard(lang)
        )

    elif data.startswith("back_"):
        lang = data.split("_")[1]

        await query.edit_message_text(
            "Қызмет таңдаңыз",
            reply_markup=main_menu_keyboard(lang)
        )

# ========================
# 🤖 AI + MESSAGE
# ========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = update.message

    # ADMIN-ға жіберу
    await context.bot.forward_message(
        ADMIN_ID,
        msg.chat_id,
        msg.message_id
    )

    # AI жауап
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": msg.text}]
        )

        ai_reply = response.choices[0].message.content

        await msg.reply_text(ai_reply)

    except Exception as e:
        print(e)
        await msg.reply_text("✅ Қабылданды")

# ========================
# 🚀 START
# ========================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот іске қосылды ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
