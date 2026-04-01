import logging
import openai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes,
)

# ========================
# ⚙️ НАСТРОЙКИ
# ========================
BOT_TOKEN = "8754227384:AAEUXtTBoOVajScixmGg-ccRV086mUQ5zrw"
ADMIN_ID = 1313252587

OPENAI_API_KEY = "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"

BUSINESS_NAME = "Сенің идеяң — біздің өнер 🎨"

KASPI_NUMBER = "+77474513371"
KASPI_NAME = "Сабира С"

openai.api_key = OPENAI_API_KEY

# ========================
# LOGGING
# ========================
logging.basicConfig(level=logging.INFO)

# ========================
# KEYBOARDS
# ========================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🖼 Фото", callback_data="photo")],
        [InlineKeyboardButton("🎬 Видео", callback_data="video")],
        [InlineKeyboardButton("🤖 AI көмек", callback_data="ai")],
        [InlineKeyboardButton("📞 Менеджер", callback_data="manager")]
    ])

def back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Артқа", callback_data="back")]
    ])

# ========================
# START
# ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👋 *{BUSINESS_NAME}*\n\nҚош келдіңіз!\nҚызмет таңдаңыз 👇",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

# ========================
# CALLBACK
# ========================
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "photo":
        await query.edit_message_text(
            "🖼 Фото жасау\n\n💰 Баға: 2000 ₸\n\nТөлем жасаңыз 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💳 Kaspi төлеу", callback_data="pay")],
                [InlineKeyboardButton("⬅️ Артқа", callback_data="back")]
            ])
        )

    elif data == "video":
        await query.edit_message_text(
            "🎬 Видео жасау\n\n💰 Баға: 5000 ₸\n\nТөлем жасаңыз 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💳 Kaspi төлеу", callback_data="pay")],
                [InlineKeyboardButton("⬅️ Артқа", callback_data="back")]
            ])
        )

    elif data == "pay":
        await query.edit_message_text(
            f"📱 Kaspi аудару:\n\n"
            f"📞 {KASPI_NUMBER}\n"
            f"👤 {KASPI_NAME}\n\n"
            f"Скриншот жіберіңіз ✅"
        )

    elif data == "manager":
        await query.edit_message_text(
            f"📞 Менеджер:\n{KASPI_NUMBER}",
            reply_markup=back_keyboard()
        )

    elif data == "ai":
        await query.edit_message_text(
            "🤖 AI-ға сұрақ жазыңыз (мәтін жіберіңіз)",
            reply_markup=back_keyboard()
        )
        context.user_data["ai_mode"] = True

    elif data == "back":
        context.user_data["ai_mode"] = False
        await query.edit_message_text(
            "Қызмет таңдаңыз 👇",
            reply_markup=main_menu()
        )

# ========================
# MESSAGE HANDLER
# ========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = update.message

    # AI режим
    if context.user_data.get("ai_mode"):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": msg.text}]
            )
            await msg.reply_text(response["choices"][0]["message"]["content"])
        except Exception as e:
            await msg.reply_text("AI қатесі 😢")
        return

    # ADMIN-ге жіберу
    await context.bot.send_message(
        ADMIN_ID,
        f"👤 {user.full_name}\n@{user.username}"
    )

    await context.bot.forward_message(
        ADMIN_ID,
        msg.chat_id,
        msg.message_id
    )

    await msg.reply_text("✅ Қабылданды! Менеджер жауап береді.")

# ========================
# MAIN
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
