Python 3.13.3 (tags/v3.13.3:6280bb5, Apr  8 2025, 14:47:33) [MSC v.1943 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ========================
# ⚙️ БАПТАУ
# ========================
BOT_TOKEN ="8754227384:AAEUXtTBoOVajScixmGg-ccRV086mUQ5zrw"
ADMIN_ID ="1313252587" 

KASPI_NUMBER ="+77474513371"
KASPI_NAME ="Сабира С"

logging.basicConfig(level=logging.INFO)

# ========================
# 🚀 /start
# ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"💳 Төлем жасау үшін:\n\n"
        f"Kaspi: {+77474513371}\n"
...         f"Аты: {Сабира С}\n\n"
...         f"✅ Төлем жасаған соң скрин жіберіңіз"
...     )
... 
... # ========================
... # 📨 СКРИН ҚАБЫЛДАУ
... # ========================
... async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
...     user = update.effective_user
...     msg = update.message
... 
...     # Админге жіберу
...     await context.bot.send_message(
...         ADMIN_ID,
...         f"👤 {user.full_name}\n@{Sabira1221}"
...     )
... 
...     await context.bot.forward_message(
...         ADMIN_ID,
...         msg.chat_id,
...         msg.message_id
...     )
... 
...     await msg.reply_text("✅ Қабылданды, рахмет!")
... 
... # ========================
... # ▶️ START
... # ========================
... def main():
...     app = Application.builder().token(BOT_TOKEN)().build()
... 
...     app.add_handler(CommandHandler("start", start))
...     app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))
... 
...     print("Бот іске қосылды ✅")
...     app.run_polling()
... 
... if __name__ == "__main__":
