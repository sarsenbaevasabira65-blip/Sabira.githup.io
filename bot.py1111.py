import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ========================
# ⚙️ БАПТАУ
# ========================
BOT_TOKEN = "8754227384:AAEUXtTBoOVajScixmGg-ccRV086mUQ5zrw"
ADMIN_ID = "1313252587"

KASPI_NUMBER = "+77474513371"
KASPI_NAME = "Сабира С"

logging.basicConfig(level=logging.INFO)

# ========================
# 🚀 /start
# ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"💳 Төлем жасау үшін:\n\n"
        f"Kaspi: {KASPI_NUMBER}\n"
        f"Аты: {KASPI_NAME}\n\n"
        f"✅ Төлем жасаған соң скрин жіберіңіз"
    )

# ========================
# 📨 СКРИН ҚАБЫЛДАУ
# ========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = update.message

    # Админге жіберу
    await context.bot.send_message(
        ADMIN_ID,
        f"👤 {user.full_name}\n@{user.username}"
    )

    await context.bot.forward_message(
        ADMIN_ID,
        msg.chat_id,
        msg.message_id
    )

    await msg.reply_text("✅ Қабылданды, рахмет!")

# ========================
# ▶️ START
# ========================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))

    print("Бот іске қосылды ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
